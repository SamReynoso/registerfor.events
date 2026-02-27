from django.conf import settings
from django.urls import reverse
from models.models import Division, Event, RegistrationItem, Team, Registration
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden

from mailbox.models import Rsvp


@login_required(login_url='/login/')
def events(request):
    registrations = Registration.objects.filter(owner=request.user)
    context = {'registrations': registrations}
    return render(request, 'host/events.html', context)


@login_required(login_url='/login/')
def registration(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if registration.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")

    context = {'registration': registration}
    return render(request, 'user/registration_details.html', context)


@login_required(login_url='/login/')
def team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")

    registrations = Registration.objects.filter(team=team)
    context = {
            'team': team,
            'registrations': registrations
            }
    return render(request, 'user/team_details.html', context)


@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.filter(owner=request.user)
    context = {'teams': teams}
    return render(request, 'user/teams.html', context)
