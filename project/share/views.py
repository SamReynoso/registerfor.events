from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed
from models.models import Event
from project.utils.phonenumber import parse_phone
from project.services.email import send_rsvp_email
from mailbox.forms import RsvpForm
from mailbox.models import Rsvp


def add_rsvp_divisions(post, rsvp, event):
    posted_keys = post.getlist('divisions[]')
    selected_divisions = []
    for division in event.divisions.all():
        if f'{division.gender}-{division.name}' in posted_keys:
            selected_divisions.append(division)

    rsvp.save()
    rsvp.divisions.add(*selected_divisions)


def authenticated_invite(request, event):
    if request.user.profile.is_complete is False:
        return HttpResponseNotAllowed(
                'Your profile is missing contact information.'
                )
    if request.method == 'POST':
        profile = request.user.profile
        rsvp = Rsvp.objects.create(
                first_name=profile.first_name,
                last_name=profile.last_name,
                email=profile.email,
                phone=profile.phone,
                recipient=request.user,
                event=event
                )
        add_rsvp_divisions(request.POST, rsvp, event)
        send_rsvp_email(rsvp)
        return redirect('explore:event', event_id=event.id)
    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'app/event_invite.html', context)


def anonymous_invite(request, event):
    if request.method == 'POST':
        data = request.POST.copy()
        data['phone'] = parse_phone(data.get('phone'), 'US')
        form = RsvpForm(data)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.save()
            add_rsvp_divisions(request, rsvp, event)
            send_rsvp_email(rsvp)
            return redirect('explore:event', event_id=event.id)
    else:
        form = RsvpForm()
    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'form': form,
            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'app/event_invite.html', context)


def event_invite(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_authenticated:
        return authenticated_invite(request, event)
    return anonymous_invite(request, event)


@xframe_options_exempt
def embedded(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'invite/embedded.html', context)


