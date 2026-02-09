from django.contrib.auth.decorators import login_required

from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from models.forms import TeamForm, TeamPhotoForm
from django.shortcuts import get_object_or_404
from models.models import Announcement, Event, Registration, Team
from project.utils.alerts import registration_withdrawn_alert_event_owner


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
            return redirect('user:team_details', team_id=team.id)
    else:
        form = TeamForm()
    context = {'form': form}
    return render(request, 'app/team_create.html', context)


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
            return redirect('user:team_details', team_id=team_id)
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
        return redirect('user:team_details', team_id=team_id)
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
            return redirect('user:team_details', team_id=team_id)
    else:
        form = TeamForm(instance=team)
    context = {'form': form}
    return render(request, 'app/team_update.html', context)


@login_required(login_url='/login/')
def team_delete(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    if request.method == 'POST':
        team.delete()
        return redirect('user:teams')
    context = {'team': team}
    return render(request, 'app/team_delete.html', context)


@login_required(login_url='/login/')
def register_for_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)

    teams = Team.objects.filter(owner=request.user).all()

    available_division_keys = [
            f'{division.gender}-{division.name}'
            for division in event.divisions.all()
            ]

    registered_team_ids = [
            reg.team.id
            for reg in Registration.objects.filter(
                owner=request.user, event=event)
            ]

    if request.method == 'POST':
        for team in teams:
            if request.POST.get(f'team{team.pk}') == 'on':
                Registration.objects.create(
                        owner=request.user,
                        event=event,
                        team=team,
                        assigned_division=event.divisions.get(
                            gender=team.gender,
                            name=team.division)
                        )
        return redirect('user:events')

    context = {
            'event': event,
            'available_division_keys': available_division_keys,
            'registered_team_ids': registered_team_ids,
            'teams': teams,
            }

    return render(request, 'app/register_for_event.html', context)


@login_required(login_url='/login/')
def registration_withdraw(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if request.method == 'POST':
        registration_withdrawn_alert_event_owner(registration)
        registration.delete()
        return redirect('user:events')
    context = {'registration': registration}
    return render(request, 'app/registration_withdraw.html', context)


@login_required(login_url='/login/')
def announcement_delete(request, announcement_id: int):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if announcement.recipient != request.user:
        return HttpResponseForbidden("You don't own this announcement.")
    if request.method == 'POST':
        announcement.delete()
        return redirect('mailbox:announcements')
    context = {'announcement': announcement}
    return render(request, 'app/announcement_delete.html', context)
