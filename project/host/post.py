from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from models.forms import EventForm, EventPosterForm
from django.http import HttpResponseForbidden
from mailbox.models import Announcement, Rsvp
from project.services.email import SendEmail
from mailbox.forms import AnnouncementForm
from project.services.alerts import Alerts
from models.divisions import DivisionCRUD
from models.registrations import RegCRUD
from models.events import EventCRUD
from django.urls import reverse
from models.models import (
        Division,
        Event,
        Registration
        )
from project.choices import (
        DivisionChoices,
        Genders,
        )


@login_required(login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            EventCRUD.save(event)
            Alerts.event_created(event)
            SendEmail.event_created(event.owner)
            return redirect('host:event', event_id=event.id)
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'host/post/event_create.html', context)


@login_required(login_url='/login/')
def event_update(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            EventCRUD.save(event)
            return redirect('host:event', event_id=event_id)
    else:
        form = EventForm(instance=event)
    context = {'event': event, 'form': form}
    return render(request, 'host/post/event_update.html', context)


@login_required(login_url='/login/')
def event_delete(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    if request.method == 'POST':
        EventCRUD.delete(event)
        return redirect('host:hosting')
    context = {'event': event}
    return render(request, 'host/post/event_delete.html', context)


@login_required(login_url='/login/')
def event_poster_update(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    if request.method == 'POST':
        form = EventPosterForm(
                request.POST,
                request.FILES,
                instance=event
                )
        if form.is_valid():
            form.save()
            return redirect('host:event', event_id=event_id)
    else:
        form = EventPosterForm(instance=event)
    context = {
            'current': event.get_poster_url(),
            'form': form
               }
    return render(request, 'app/picture_update.html', context)


@login_required(login_url='/login/')
def event_poster_delete(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    if request.method == 'POST':
        event.poster.delete(save=False)
        event.save()
        return redirect('host:event', event_id=event_id)
    context = {'current': event.get_poster_url()}
    return render(request, 'app/picture_delete.html', context)


@login_required(login_url='/login/')
def event_divisions(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    protected_keys = set(
            division.get_key() for division in event.divisions.all()
            )

    pre_existing_keys = [
            division.get_key()
            for division in event.divisions.all()
            ]
    existing_keys = []

    if request.method == "POST":
        posted_keys = request.POST.getlist('division[]')

        for k in posted_keys:
            if k not in existing_keys:
                name, gender = Division.split_key(k)
                new_division = DivisionCRUD.create(
                        event=event,
                        gender=gender,
                        name=name
                        )
                existing_keys.append(new_division.get_key())

        for k in pre_existing_keys:
            if k not in posted_keys and k not in protected_keys:
                name, gender = Division.split_key(k)
                division = Division.objects.get(
                        event=event,
                        gender=gender,
                        name=name
                        )
                DivisionCRUD.delete(division)
            else:
                existing_keys.append(k)

        return redirect('host:event', event_id=event.id)

    context = {
            'event': event,
            'existing_keys': existing_keys,
            'protected_keys': protected_keys,
            'division_options': {
                'genders': Genders,
                'divisions': DivisionChoices,
                }
            }

    return render(request, 'host/post/event_divisions.html', context)


def status_page(request, event_id: int, func, temp):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    if request.method == 'POST':
        func(event)
        url = reverse('host:event', args=[event.id])
        return redirect(f'{url}#lifecycle')
    context = {'event': event}
    return render(request, temp, context)


@login_required(login_url='/login/')
def status_open(request, event_id: int):
    return status_page(request,
                       event_id,
                       EventCRUD.open_registration,
                       'host/post/status_open.html')


@login_required(login_url='/login/')
def status_close(request, event_id: int):
    return status_page(request,
                       event_id,
                       EventCRUD.close_registration,
                       'host/post/status_close.html')


@login_required(login_url='/login/')
def status_scheduled(request, event_id: int):
    return status_page(request,
                       event_id,
                       EventCRUD.mark_as_scheduled,
                       'host/post/status_scheduled.html')


@login_required(login_url='/login/')
def event_announcement_create(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    announcements = []
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            for reg in event.registrations.all():
                announcements.append(
                    Announcement(
                        sender=request.user,
                        recipient=reg.owner,
                        title=form.cleaned_data['title'],
                        body=form.cleaned_data['body'],
                        event=event,
                        )
                        )
            Announcement.objects.bulk_create(announcements)
            return redirect('host:event', event_id=event_id)
    form = AnnouncementForm()
    context = {'event': event, 'form': form}
    return render(request, 'host/post/event_announcement.html', context)


@login_required(login_url='/login/')
def registration_cancel(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)

    if request.method == 'POST':
        event = registration.event
        RegCRUD.cancel(registration)
        return redirect('host:event', event_id=event.id)

    context = {'registration': registration}
    return render(request, 'host/post/registration_cancel.html', context)


@login_required(login_url='/login/')
def rsvp_convert(request, rsvp_id: int):
    rsvp = get_object_or_404(Rsvp, id=rsvp_id)
    if rsvp.event.owner != request.user:
        return HttpResponseForbidden(
                "You don't own event this rsvp belongs to."
                )
    if request.method == "POST":
        event = rsvp.event
        RegCRUD.rsvp_convert(rsvp)
        return redirect('host:invitations', event_id=event.id)

    context = {'rsvp': rsvp}
    return render(request, 'host/post/rsvp_convert.html', context)


@login_required(login_url='/login/')
def rsvp_cancel(request, rsvp_id: int):
    context = {}
    return render(request, 'host/post/rsvp_cancel.html', context)

