from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from models.models import Event, Team


def account(request):
    print(request.user.is_authenticated)
    return render(request, 'user/account.html')


@login_required(login_url='/login/')
def events(request):
    return render(request, 'user/events.html')


@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.filter(owner=request.user)
    context = {'teams': teams}
    return render(request, 'user/teams.html', context)


@login_required(login_url='/login/')
def hosting(request):
    return render(request, 'user/hosting.html')


@login_required(login_url='/login/')
def participants(request):
    return render(request, 'user/participants.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'user/profile.html')


@login_required(login_url='/login/')
def event_details(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    context = {'event': event}
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    return render(request, 'user/event_details.html', context)


@login_required(login_url='/login/')
def team_details(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    context = {'team': team}
    return render(request, 'user/team_details.html', context)
