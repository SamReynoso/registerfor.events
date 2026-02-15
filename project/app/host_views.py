from project.utils.alerts import host_canceled_registration_alert_team_owner
from project.services.email import send_registration_canceled_email
from project.services.email import send_host_new_registration_email
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from models.forms import EventForm, EventPosterForm
from django.http import HttpResponseForbidden
from mailbox.forms import AnnouncementForm
from mailbox.models import Announcement, Rsvp
from models.models import (
        Division,
        DivisionChoices,
        Event,
        Genders,
        Registration
        )


@login_required(login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event = form.save()
            return redirect('user:hosting_event', event_id=event.id)
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'app/event_create.html', context)


@login_required(login_url='/login/')
def event_update(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('user:event_details', event_id=event_id)
    else:
        form = EventForm(instance=event)
    context = {'event': event, 'form': form}
    return render(request, 'app/event_update.html', context)


@login_required(login_url='/login/')
def event_delete(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    if request.method == 'POST':

        event.delete()
        return redirect('user:hosting')
    context = {'event': event}
    return render(request, 'app/event_delete.html', context)


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
            return redirect('user:hosting_event', event_id=event_id)
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
        event.poster = None
        event.save()
        return redirect('user:hosting_event', event_id=event_id)
    context = {'current': event.get_poster_url()}
    return render(request, 'app/picture_delete.html', context)


@login_required(login_url='/login/')
def event_divisions(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    existing_keys = [
            f"{division.gender}-{division.name}"
            for division in event.divisions.all()
            ]

    if request.method == "POST":
        posted_keys = request.POST.getlist('division[]')

        for k in posted_keys:
            gender, division_name = k.split('-')
            if k not in existing_keys:
                new_division = Division.objects.create(event=event,
                                                       gender=gender,
                                                       name=division_name)
                existing_keys.append(
                        f'{new_division.gender}-{new_division.name}')
        for k in existing_keys:
            gender, division_name = k.split('-')
            if k not in posted_keys:
                Division.objects.get(event=event,
                                     gender=gender,
                                     name=division_name).delete()
                existing_keys.remove(k)
        return redirect('user:hosting_event', event_id=event.id)

    division_options = {
            'genders': Genders,
            'divisions': DivisionChoices,
            }

    protected_keys = set()
    for registration in event.registrations.all():
        k = f'{registration.team.gender}-{registration.team.division}'
        protected_keys.add(k)
    context = {
            'event': event,
            'division_options': division_options,
            'existing_keys': existing_keys,
            'protected_keys': protected_keys,
            }

    return render(request, 'app/event_divisions.html', context)


@login_required(login_url='/login/')
def participant_edit(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if request.method == 'POST':
        host_canceled_registration_alert_team_owner(registration)
        send_registration_canceled_email(registration)
        registration.delete()
        return redirect('user:hosting_division',
                        division_id=registration.assigned_division.id)
    context = {'registration': registration}
    return render(request, 'app/event_participant_edit.html', context)


@login_required(login_url='/login/')
def event_status(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    if request.method == 'POST':
        event.public = not event.public
        event.save()
        return redirect('user:hosting_event', event_id=event.id)
    context = {'event': event}
    return render(request, 'app/event_status.html', context)


@login_required(login_url='/login/')
def event_announcement(request, event_id: int):
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
            return redirect('user:hosting_event', event_id=event_id)
    form = AnnouncementForm()
    context = {'event': event, 'form': form}
    return render(request, 'app/event_announcement.html', context)


@login_required(login_url='/login/')
def event_invite_creaet(request, event_id: int):
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
            return redirect('user:hosting_event', event_id=event_id)
    form = AnnouncementForm()
    context = {'event': event, 'form': form}
    return render(request, 'app/event_announcement.html', context)


@login_required(login_url='/login/')
def rsvp_convert(request, rsvp_id: int):
    rsvp = get_object_or_404(Rsvp, id=rsvp_id)
    if rsvp.event.owner != request.user:
        return HttpResponseForbidden(
                "You don't own event this rsvp belongs to."
                )
    if request.method == "POST":
        owner = rsvp.recipient
        for division in rsvp.divisions.all():
            registration = Registration.objects.create(
                    owner=owner,
                    assigned_division=division,
                    event=rsvp.event,
                    first_name=rsvp.first_name,
                    last_name=rsvp.last_name,
                    email=rsvp.email,
                    phone=rsvp.phone,
                    )
            send_host_new_registration_email(registration)
        rsvp.delete()
        return redirect('user:hosting_invitations', event_id=rsvp.event.id)
    context = {'rsvp': rsvp}
    return render(request, 'app/rsvp_convert.html', context)
