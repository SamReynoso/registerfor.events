from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from models.forms import EventForm, TeamForm
from django.shortcuts import get_object_or_404
from models.models import Event, Registration, Team


@login_required(login_url='/login/')
def create(request):
    return render(request, 'create/create.html')


@login_required(login_url='/login/')
def events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event = form.save()
            return redirect('user:event_details', event_id=event.id)
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'create/events.html', context)


@login_required(login_url='/login/')
def teams(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.save()
            return redirect('user:team_details', team_id=team.id)
    else:
        form = TeamForm()
    context = {'form': form}
    return render(request, 'create/teams.html', context)


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

        return redirect('details:event', event_id=event_id)

    context = {
            'event': event,
            'available_division_keys': available_division_keys,
            'registered_team_ids': registered_team_ids,
            'teams': teams,
            }

    return render(request, 'create/register_for_event.html', context)
