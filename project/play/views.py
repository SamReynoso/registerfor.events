from models.models import RegistrationItem, Team, Registration
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden


@login_required(login_url='/login/')
def events(request):
    registrations = Registration.objects.filter(owner=request.user)
    context = {'registrations': registrations}
    return render(request, 'play/events.html', context)


@login_required(login_url='/login/')
def team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    if team.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")

    items = RegistrationItem.objects.filter(team=team)
    context = {
            'team': team,
            'items': items
            }
    return render(request, 'play/team.html', context)


@login_required(login_url='/login/')
def teams(request):
    teams = Team.objects.filter(owner=request.user)
    context = {'teams': teams}
    return render(request, 'play/teams.html', context)


@login_required(login_url='/login/')
def registration(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if registration.owner != request.user:
        return HttpResponseForbidden("You don't own this team.")

    context = {'registration': registration}
    return render(request, 'play/registration.html', context)


@login_required(login_url='/login/')
def registration_item(request, registration_item_id: int):
    item = get_object_or_404(RegistrationItem, id=registration_item_id)
    if item.registration.owner != request.user:
        return HttpResponseForbidden("You don't own this registraiton.")

    context = {'item': item}
    return render(request, 'play/registration_item.html', context)
