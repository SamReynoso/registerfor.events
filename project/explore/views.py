from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from project.choices import (
        Cities,
        Genders,
        DivisionChoices,
        Sports,
        States,
        )
from models.models import (
        Profile,
        Event,
        Team,
        Division,
        Registration,
        )


def profile(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    context = {'profile': profile}
    return render(request, 'explore/profile.html', context)


def event(request, event_id: int):
    event = Event.objects.get(id=event_id)
    registrations = Registration.objects.filter(event=event).all()
    context = {
            'event': event,
            'registrations': registrations
            }
    return render(request, 'explore/event.html', context)


def team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    context = {'team': team}
    return render(request, 'explore/team.html', context)


def division(request, division_id: int):
    division = get_object_or_404(Division, id=division_id)
    context = {'division': division}
    return render(request, 'explore/division.html', context)


def search_results(request):
    context = {}
    search_options = {
            'sports': Sports,
            'cities': Cities,
            'states': States,
            'divisions': DivisionChoices,
            'genders': Genders,
            }
    qs = Event.objects.all()
    query = request.GET
    if query:
        sport = query.get('sport')
        city = query.get('city')
        state = query.get('state')
        divisions = list(query.getlist('division[]'))

        gender = query.get('gender')
        # radius = 'all'
        # date_range = query.get('city')

        all_or_none = ['all', None]
        if sport not in all_or_none:
            qs = qs.filter(sport=sport)

        if city not in all_or_none:
            qs = qs.filter(city__iexact=city)

        if state not in all_or_none:
            qs = qs.filter(state=state)

        if len(divisions) != 0:
            if 'all' not in divisions:
                qs = qs.filter(divisions__name__in=divisions)

        if gender not in all_or_none:
            qs = qs.filter(divisions__gender=gender)

    paginator = Paginator(qs, 19)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
            'search_options': search_options,
            'page_obj': page_obj
            }
    return render(request, 'explore/search_results.html', context)
