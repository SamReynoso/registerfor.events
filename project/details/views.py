from django.shortcuts import render
from django.shortcuts import get_object_or_404

from models.models import (
        Profile,
        Event,
        Team,
        Division,
        Registration,
        Genders,
        DivisionChoices,
        Sports,
        States,
        )


def profile(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    context = {'profile': profile}
    return render(request, 'details/profile.html', context)


def event(request, event_id: int):
    event = Event.objects.get(id=event_id)
    registrations = Registration.objects.filter(event=event).all()
    context = {
            'event': event,
            'registrations': registrations
            }
    return render(request, 'details/event.html', context)


def team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    context = {'team': team}
    return render(request, 'details/team.html', context)


def division(request, division_id: int):
    division = get_object_or_404(Division, id=division_id)
    context = {'division': division}
    return render(request, 'details/division.html', context)


def search_results(request):
    context = {}
    search_options = {
            'sports': Sports,
            'divisions': DivisionChoices,
            'genders': Genders,
            'states': States,
            }
    if request.method == 'GET':
        qs = Event.objects.all()
        query = request.GET
        if query:
            sport = query.get('sport')
            city = query.get('city')
            state = query.get('state')
            gender = query.get('gender')
            divisions = query.getlist('division[]')
            # radius = 'all'
            # date_range = query.get('city')

            all_or_none = ['all', None]
            if sport not in all_or_none:
                qs = qs.filter(sport=sport)

            if city not in all_or_none:
                qs = qs.filter(city__iexact=city)

            if state not in all_or_none:
                qs = qs.filter(state=state)

            if gender not in all_or_none:
                qs = qs.filter(divisions__gender=gender)

            if 'all' not in divisions or len(divisions) != 0:
                if gender == 'all':
                    qs = qs.filter(divisions__name__in=divisions)
                else:
                    qs = qs.filter(divisions__name__in=divisions,
                                   divisions__gender=gender)
    #        if start_date:
    #            qs = qs.filter(start_date__gte=start_date)
        print(qs)
        context = {
                'search_options': search_options,
                'events': qs.all()
                }
    return render(request, 'details/search_results.html', context)
