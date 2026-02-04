from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from models.forms import EventForm, TeamForm


@login_required(login_url='/login/')
def create(request):
    return render(request, 'create/create.html')


@login_required(login_url='/login/')
def events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('user:event_details', event_id=event.id)
    else:
        form = EventForm()
    context = {'form': form}
    return render(request, 'create/events.html', context)


@login_required(login_url='/login/')
def teams(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.save()
            return redirect('user:team_details', team_id=team.id)
    else:
        form = TeamForm()
    context = {'form': form}
    return render(request, 'create/teams.html', context)
