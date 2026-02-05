''' details app'''

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from models.models import Event, Registration, Team, Profile


def profile(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    context = {'profile': profile}
    return render(request, 'details/profile.html', context)


def event(request, event_id: int):
    event = Event.objects.get(id=event_id)
    registrations = Registration.objects.filter(event=event).all()
    print(registrations)
    context = {
            'event': event,
            'registrations': registrations
            }
    return render(request, 'details/event.html', context)


def team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    context = {'team': team}
    return render(request, 'details/team.html', context)
