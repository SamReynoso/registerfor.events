from django.utils.http import url_has_allowed_host_and_scheme
from project.utils.alerts import registration_withdrawn_alert_event_owner
from django.contrib.auth.decorators import login_required
from models.models import Event, Registration, RegistrationItem, Team
from models.forms import TeamForm, TeamPhotoForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from project.services.email import (
        send_host_new_registration_email,
        send_participant_new_registration_email,
        send_registration_withdrawn_email,
        )
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


@login_required(login_url='/login/')
def register_for_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    event_division_keys = [
            division.get_key()
            for division in event.divisions.all()
            ]

    print(event_division_keys)

    registration = Registration.objects.filter(
            owner=request.user, event=event
            ).first()

    if registration is not None:
        registered_teams = registration.teams  # add .all() for consistence
    else:
        registered_teams = []

    teams = Team.objects.filter(owner=request.user).all()

    if request.method == 'POST':
        if request.user.profile.is_complete is False:
            return HttpResponseForbidden('Your profile is incomplete.')

        if registration is None:
            registration = Registration.objects.create_from_objects(
                    owner=request.user,
                    event=event
                    )

        modified = False
        for team in teams:
            if request.POST.get(f'team{team.id}') == 'on':
                division = event.divisions.get(
                        gender=team.gender,
                        name=team.division)

                RegistrationItem.objects.create(
                        registration=registration,
                        team=team,
                        division=division,
                        unit_price=division.unit_price,
                        invoice=registration.invoice
                        )
                modified = True
        if modified and registration.invoice:
            registration.invoice.status = InvoiceStatus.MODIFIED
            registration.invoice.save()

        send_host_new_registration_email(registration)
        send_participant_new_registration_email(registration)
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
