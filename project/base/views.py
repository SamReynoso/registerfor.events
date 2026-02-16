from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout, authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from models.models import Event, Profile
from project.utils.phonenumber import parse_phone
from project.services.email import (
        send_rsvp_email,
        send_signup_email_verification_email,
        )
from models.forms import RegisterForm
from mailbox.forms import RsvpForm
from django.conf import settings
from mailbox.models import Rsvp
from django.urls import reverse


User = get_user_model()


def home_view(request):
    return render(request, 'base/home.html')


def test_view(request):
    reg = Rsvp.objects.all().first()
    context = {'rsvp': reg}
    return render(request, 'email/rsvp_email.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            user.refresh_from_db()
            profile = Profile.objects.create(user=user)
            profile.save()
            send_signup_email_verification_email(user)
            return redirect('base:login')
    else:
        form = RegisterForm()

    return render(request, 'base/register.html', {'form': form})


def verify_email(_, uidb64: str, token: str):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("base:login")
    else:
        return redirect("base:register")


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('user:account')
        else:
            error = 'Invalid credentials'
    return render(request, 'base/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('base:login')


def event_invite_sharable(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    site_url = settings.SITE_URL
    context = {
            'event': event,
            'site_url': site_url,
            'sharable_url': (
                site_url
                + reverse('base:invite', kwargs={'event_id': event_id})
                )
               }
    return render(request, 'base/invite_sharable.html', context)


def add_rsvp_divisions(request, rsvp, event):
    posted_keys = request.POST.getlist('divisions[]')
    selected_divisions = []
    for division in event.divisions.all():
        if f'{division.gender}-{division.name}' in posted_keys:
            selected_divisions.append(division)

    rsvp.save()
    rsvp.divisions.add(*selected_divisions)


def authenticated_invite(request, event):
    if request.user.profile.is_complete is False:
        return HttpResponseNotAllowed(
                'Your profile is missing contact information.'
                )
    if request.method == 'POST':
        profile = request.user.profile
        rsvp = Rsvp.objects.create(
                first_name=profile.first_name,
                last_name=profile.last_name,
                email=profile.email,
                phone=profile.phone,
                recipient=request.user,
                event=event
                )
        add_rsvp_divisions(request, rsvp, event)
        send_rsvp_email(rsvp)
        return redirect('details:event', event_id=event.id)
    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'base/invite.html', context)


def anonymous_invite(request, event):
    if request.method == 'POST':
        data = request.POST.copy()
        data['phone'] = parse_phone(data.get('phone'), 'US')
        form = RsvpForm(data)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.save()
            add_rsvp_divisions(request, rsvp, event)
            send_rsvp_email(rsvp)
            return redirect('details:event', event_id=event.id)
    else:
        form = RsvpForm()
    context = {
            'site_url': settings.SITE_URL,
            'event': event,
            'form': form,
            'subject': f'{event.name} Invitation',
            'disctiption': f'Join us on {event.start_date} in {event.city}.'
               }
    return render(request, 'base/invite.html', context)


def event_invite(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_authenticated:
        return authenticated_invite(request, event)
    return anonymous_invite(request, event)
