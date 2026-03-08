from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import get_object_or_404, render, redirect
from project.utils.phonenumber import parse_phone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from project.services.email import SendEmail
from mailbox.forms import RsvpForm
from django.conf import settings
from mailbox.models import Rsvp
from models.models import Event


@xframe_options_exempt
def embedded(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'share/embedded.html', context)


def add_rsvp_divisions(post, rsvp, event):
    posted_keys = post.getlist('divisions[]')
    selected_divisions = []
    print('posted_keys', posted_keys)
    for division in event.divisions.all():
        print('division_key', division.get_key())
        if division.get_key() in posted_keys:
            print('found key')
            selected_divisions.append(division)
    rsvp.divisions.add(*selected_divisions)
    rsvp.save()



@login_required(login_url='/login/')
def event_invite(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if request.user.profile.is_complete is False:
        return HttpResponseNotAllowed(
                'Your profile is missing contact information.'
                )
    if request.method == 'POST':
        profile = request.user.profile
        rsvp = Rsvp.objects.create(
                owner=event.owner,
                sender=request.user,
                event=event,

                first_name=profile.first_name,
                last_name=profile.last_name,
                email=request.user.email,
                phone=profile.phone,
                )
        add_rsvp_divisions(request.POST, rsvp, event)
        print(rsvp.divisions.all())
        # send_rsvp_email(rsvp)
        return redirect('explore:event', event_id=event.id)

    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'share/event_invite.html', context)


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
            # send_rsvp_email(rsvp)
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
    return render(request, 'share/event_invite.html', context)
