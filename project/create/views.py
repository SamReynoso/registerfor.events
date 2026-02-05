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
    registered_teams = Registration.objects.filter(event=event)
    print('---->', registered_teams)
    registered_team_ids = registered_teams.values_list('team_id', flat=True)
    available_teams = Team.objects.filter(owner=request.user).exclude(
        id__in=registered_team_ids)

    # Possible add a check here that all teams can be create before committing
    # anting to the database
    if request.method == 'POST':
        for team in available_teams:
            if request.POST.get(f'team{team.pk}') == 'on':
                Registration.objects.create(owner=request.user,
                                            event=event,
                                            team=team)
        return redirect('user:event_details', event_id=event_id)
    context = {
            'event': event,
            'teams': available_teams,
            'registered_teams': registered_teams
            }
    return render(request, 'create/register_for_event.html', context)
