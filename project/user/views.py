from models.models import Division, Event, Team, Registration
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden

from mailbox.models import Rsvp


@login_required(login_url='/login/')
def account(request):
    return render(request, 'user/account.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'user/profile.html')


@login_required(login_url='/login/')
def events(request):
    registrations = Registration.objects.filter(owner=request.user)
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
def hosting_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    divisions = Division.objects.filter(event=event)
    context = {
            'event': event,
            'divisions': divisions,
            }
    return render(request, 'user/hosting_event.html', context)


@login_required(login_url='/login/')
def hosting_invitations(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    rsvps = Rsvp.objects.filter(event=event)
    context = {
            'event': event,
            'rsvps': rsvps,
            }
    return render(request, 'user/hosting_invitations.html', context)


@login_required(login_url='/login/')
def hosting_division(request, division_id: int):
    division = Division.objects.get(id=division_id)
    context = {'division': division}
    return render(request, 'user/hosting_division.html', context)


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
