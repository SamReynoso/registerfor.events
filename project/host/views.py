from django.conf import settings
from django.urls import reverse
from models.models import Division, Event, RegistrationItem, Registration
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden

from mailbox.models import Rsvp


@login_required(login_url='/login/')
def hosting(request):
    events = Event.objects.filter(owner=request.user)
    context = {'events': events}
    return render(request, 'host/hosting.html', context)


@login_required(login_url='/login/')
def event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    divisions = Division.objects.filter(event=event)
    context = {
            'event': event,
            'divisions': divisions,
            }
    return render(request, 'host/event.html', context)


@login_required(login_url='/login/')
def division(request, division_id: int):
    division = Division.objects.get(id=division_id)
    context = {'division': division}
    return render(request, 'host/division.html', context)


@login_required(login_url='/login/')
def registration(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if registration.event.owner != request.user:
        return HttpResponseForbidden(
                "You don't own this registration's event."
                )
    context = {'registration': registration}
    return render(request, 'host/registration.html', context)


@login_required(login_url='/login/')
def registration_item(request, registration_item_id: int):
    print('hello')
    item = get_object_or_404(RegistrationItem, id=registration_item_id)
    if item.registration.owner != request.user:
        return HttpResponseForbidden(
                "You don't own this item's registration's event."
                )
    context = {
            'item': item
            }
    return render(request, 'host/registration_item.html', context)


@login_required(login_url='/login/')
def embed(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    context = {
            'site_url': settings.SITE_URL,
            'event': event
            }
    return render(request, 'host/embed.html', context)


@login_required(login_url='/login/')
def invitations(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    rsvps = Rsvp.objects.filter(event=event)

    context = {
            'event': event,
            'rsvps': rsvps,
            }
    return render(request, 'host/invitations.html', context)


@login_required(login_url='/login/')
def invite(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    site_url = settings.SITE_URL
    context = {
            'event': event,
            'site_url': site_url,
            'sharable_url': (
                site_url
                + reverse('share:event_invite', kwargs={'event_id': event_id})
                )
               }
    return render(request, 'host/invite.html', context)
