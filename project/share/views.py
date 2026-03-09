from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import get_object_or_404, render, redirect
from models.registrations import RegCRUD
from project.choices import DivisionChoices, Genders
from project.services.alerts import Alerts
from project.utils.phonenumber import parse_phone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from project.services.email import SendEmail
from mailbox.forms import RsvpForm
from django.conf import settings
from mailbox.models import Rsvp
from models.models import Division, Event, Team
from project.utils.registration_ops import RegistrationOps


@xframe_options_exempt
def embedded(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'share/embedded.html', context)


def add_rsvp_divisions(post, rsvp, event):
    posted_keys = post.getlist('divisions[]')
    selected_divisions = []
    for division in event.divisions.all():
        if division.get_key() in posted_keys:
            selected_divisions.append(division)
    rsvp.divisions.add(*selected_divisions)
    rsvp.save()



@login_required(login_url='/login/')
def authenticated_rsvp(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if request.user.profile.is_complete is False:
        return HttpResponseNotAllowed(
                'Your profile is missing contact information.'
                )
    event_division_keys = RegistrationOps.get_event_division_keys(event)
    registration = RegistrationOps.get_current_registration(request.user, event)
    registered_teams = RegistrationOps.get_registered_teams(registration)
    teams = Team.objects.filter(owner=request.user).all()

    if request.method == 'POST':
        added_teams = []
        rsvp_teams = []
        for team in teams:
            if request.POST.get(f'team{team.id}') == 'on':
                added_teams.append(team)
            if request.POST.get(f'rsvp{team.id}') == 'on':
                rsvp_teams.append(team)


        if registration is None and added_teams:
            registration = RegCRUD.create(owner=request.owner, event=event)

        if added_teams:
            assert registration is not None
            RegCRUD.bulk_create_items(registration, added_teams)
            SendEmail.host_registration(registration)
            Alerts.new_registration(registration)

        if rsvp_teams:
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
            rsvp.teams.add(*rsvp_teams)
            SendEmail.rsvp(rsvp)
            Alerts.rsvp_created(rsvp)
        return redirect('explore:event', event_id=event.id)

    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'teams': teams,
            'registered_teams': registered_teams,
            'event_division_keys': event_division_keys,

            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.',
               }
    return render(request, 'share/event_rsvp.html', context)


def anonymous_rsvp(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
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
            'genders': Genders,
            'division_choices': DivisionChoices,

            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'share/event_rsvp.html', context)


def event_rsvp(request, event_id: int):
    if request.user.is_authenticated:
        return redirect('share:auth_rsvp', event_id=event_id)
    return redirect('share:no_auth_rsvp', event_id=event_id)
