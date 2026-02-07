from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from models.forms import EventForm
from models.models import Division, DivisionChoices, Event, Gender, Registration


@login_required(login_url='/login/')
def event_create(request):
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
    return render(request, 'app/event_create.html', context)


@login_required(login_url='/login/')
def event_divisions(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")

    existing_keys = [
            f"{division.gender}-{division.name}"
            for division in event.divisions.all()
            ]

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
        return redirect('user:event_details', event_id=event.id)

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
def participant_edit(request, registration_id: int):
    registration = get_object_or_404(Registration, id=registration_id)
    if request.method == 'POST':
        event_id = registration.event.id
        registration.delete()
        return redirect('user:hosting_participants', event_id=event_id)
    context = {'registration': registration}
    return render(request, 'app/participant_edit.html', context)
