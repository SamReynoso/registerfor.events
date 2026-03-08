from django.utils.http import url_has_allowed_host_and_scheme
from models.registrations import RegCRUD
from project.services.alerts import Alerts
from project.services.email import SendEmail
from project.utils.alerts import registration_withdrawn_alert_event_owner
from django.contrib.auth.decorators import login_required
from models.models import Event, Registration, RegistrationItem, Team
from models.forms import TeamForm, TeamPhotoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from project.choices import InvoiceStatus


@login_required(login_url='/login/')
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.save()
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('play:team', team_id=team.id)
    else:
        form = TeamForm()
    context = {'form': form}
    return render(request, 'play/post/team_create.html', context)


@login_required(login_url='/login/')
def team_photo_update(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    if request.method == 'POST':
        form = TeamPhotoForm(
                request.POST,
                request.FILES,
                instance=team
                )
        if form.is_valid():
            form.save()
            return redirect('play:team', team_id=team_id)
    else:
        form = TeamPhotoForm(instance=team)
    context = {
            'current': team.get_photo_url(),
            'form': form
               }
    return render(request, 'app/picture_update.html', context)


@login_required(login_url='/login/')
def team_photo_delete(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    if request.method == 'POST':
        team.photo = None
        team.save()
        return redirect('play:team', team_id=team_id)
    context = {'current': team.get_photo_url()}
    return render(request, 'app/picture_delete.html', context)


@login_required(login_url='/login/')
def team_update(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('play:team', team_id=team_id)
    else:
        form = TeamForm(instance=team)
    context = {'form': form}
    return render(request, 'play/post/team_update.html', context)


@login_required(login_url='/login/')
def team_delete(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    if request.method == 'POST':
        team.delete()
        return redirect('user:teams')
    context = {'team': team}
    return render(request, 'play/post/team_delete.html', context)


class RegisterForOps:
    @staticmethod
    def get_event_division_keys(event: Event):
        return [ division.get_key() for division in event.divisions.all() ]

    @staticmethod
    def get_current_registration(owner, event: Event):
        return Registration.objects.filter(owner=owner, event=event).first()

    @staticmethod
    def get_registered_teams(registration):
        if registration is not None:
            if registration.items.all():
                return [item.team for item in registration.items.all()]
        return []



@login_required(login_url='/login/')
def register_for_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)

    event_division_keys = RegisterForOps.get_event_division_keys(event)
    registration = RegisterForOps.get_current_registration(request.user, event)
    registered_teams = RegisterForOps.get_registered_teams(registration)
    teams = Team.objects.filter(owner=request.user).all()

    if request.method == 'POST':
        if request.user.profile.is_complete is False:
            return HttpResponseForbidden('Your profile is incomplete.')

        if registration is None:
            registration = RegCRUD.create(owner=request.user, event=event)

        added_teams = []
        for team in teams:
            if request.POST.get(f'team{team.id}') == 'on':
                added_teams.append(team)
        RegCRUD.bulk_create_items(registration, added_teams)
        SendEmail.host_registration(registration)
        Alerts.new_registrationel(registration)

        return redirect('play:registration', registration_id=registration.id)

    context = {
            'event': event,
            'registration': registration,
            'teams': teams,
            'registered_teams': registered_teams,
            'event_division_keys': event_division_keys,
            }

    return render(request, 'play/post/register_for_event.html', context)


@login_required(login_url='/login/')
def registration_modify(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)

    items = registration.items.all()

    if request.method == 'POST':
        profile = request.user.profile
        if profile.is_complete is False:
            return HttpResponseForbidden('Your profile is incomplete.')

        for item in items:
            if request.POST.get(f'team{item.team.id}') == 'on':
                item.delete()

        return redirect('play:registration', registration_id=registration.id)

    context = {
            'registration': registration,
            'items': items
               }

    return render(request, 'play/post/registration_update.html', context)


@login_required(login_url='/login/')
def withdraw(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if request.method == 'POST':
        # registration_withdrawn_alert_event_owner(registration)
        # send_registration_withdrawn_email(registration)
        registration.delete()
        return redirect('play:events')
    context = {'registration': registration}
    return render(request, 'play/post/withdraw.html', context)
