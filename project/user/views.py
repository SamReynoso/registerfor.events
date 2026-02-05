from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from models.models import Event, Team, Registration


@login_required(login_url='/login/')
def account(request):
    return render(request, 'user/account.html')


@login_required(login_url='/login/')
def events(request):
    registrations = Registration.objects.filter(owner=request.user)
    print(registrations)
    context = {'registrations': registrations}
    return render(request, 'user/events.html', context)


@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.filter(owner=request.user)
    context = {'teams': teams}
    return render(request, 'user/teams.html', context)


@login_required(login_url='/login/')
def hosting(request):
    events = Event.objects.filter(owner=request.user)
    context = {'events': events}
    return render(request, 'user/hosting.html', context)


@login_required(login_url='/login/')
def participants(request):
    return render(request, 'user/participants.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'user/profile.html')


@login_required(login_url='/login/')
def event_details(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    print(registrations)
    context = {
            'event': event,
            'registrations': registrations
            }
    return render(request, 'user/event_details.html', context)


@login_required(login_url='/login/')
def team_details(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    registrations = Registration.objects.filter(team=team)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")
    context = {
            'team': team,
            'registrations': registrations
            }
    return render(request, 'user/team_details.html', context)


@login_required(login_url='/login/')
def registration_details(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if registration.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")

    context = {'registration': registration}
    return render(request, 'user/registration_details.html', context)
