from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from models.forms import RegisterForm
from models.models import Event, Profile, Sports, DivisionChoices, Gender, State, Cities


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            user.refresh_from_db()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('base:login')
    else:
        form = RegisterForm()

    return render(request, 'base/register.html', {'form': form})


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user:account')
        else:
            error = 'Invalid credentials'

    return render(request, 'base/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('base:login')


def home(request):
    return render(request, 'base/home.html')


def events(request):
    events = Event.objects.all()
    search_options = {
            'sports': Sports,
            'divisions': DivisionChoices,
            'genders': Gender,
            'cities': Cities,
            'states': State
            }
    context = {
            'events': events,
            'search_options': search_options
            }
    return render(request, 'base/events.html', context)


def hosts(request):
    return render(request, 'base/hosts.html')


def teams(request):
    return render(request, 'base/teams.html')
