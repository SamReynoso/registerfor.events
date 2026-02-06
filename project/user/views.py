from django.contrib.auth.decorators import login_required
from django.db.models import Count, IntegerField, OuterRef, Subquery
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import render
from models.models import Division, Event, Team, Registration, Gender, DivisionChoices
from models.forms import ProfileForm


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
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'user/profile_update.html', context)


@login_required(login_url='/login/')
def profile_picture_update(request):
    del request
    return redirect('user:profile')


@login_required(login_url='/login/')
def event_details(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    matching_regs = Registration.objects.filter(
            event=event,
            team__gender=OuterRef('gender'),
            team__division=OuterRef('name')
            ).values('team__gender', 'team__division').annotate(
                    cnt=Count('id')
                    ).values('cnt')

    divisions = Division.objects.annotate(
            reg_count=Subquery(matching_regs, output_field=IntegerField())
            )

    registrations = Registration.objects.filter(event=event)
    context = {
            'event': event,
            'registrations': registrations,
            'divisions': divisions,
            }
    return render(request, 'user/event_details.html', context)


@login_required(login_url='/login/')
def event_divisions(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    existing_keys = [
            f"{division.gender}-{division.name}"
            for division in event.divisions.all()
            ]

    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    if request.method == "POST":
        posted_keys = request.POST.getlist('division[]')

        for k in posted_keys:
            gender, division_name = k.split('-')
            if k not in existing_keys:
                new_division = Division.objects.create(event=event,
                                                       gender=gender,
                                                       name=division_name)
                existing_keys.append(
                        f'{new_division.gender}-{new_division.name}')
                print(k, 'was added')
        for k in existing_keys:
            gender, division_name = k.split('-')
            if k not in posted_keys:
                Division.objects.get(event=event,
                                     gender=gender,
                                     name=division_name).delete()
                existing_keys.remove(k)
                print(k, 'was deleted')

    division_options = {
            'genders': Gender,
            'divisions': DivisionChoices,
            }

    protected_keys = set()
    for registration in event.registrations.all():
        k = f'{registration.team.gender}-{registration.team.division}'
        protected_keys.add(k)
    context = {
            'event': event,
            'division_options': division_options,
            'existing_keys': existing_keys,
            'protected_keys': protected_keys,
            }

    return render(request, 'user/event_divisions.html', context)


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
