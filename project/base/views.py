from django.shortcuts import get_object_or_404, render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout, authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from models.models import Event, Profile
from project.services.email import SendEmail
from models.forms import RegisterForm
from django.conf import settings
from mailbox.models import Rsvp
from django.urls import reverse
import logging
from project.services.email import SendEmail


User = get_user_model()

logger = logging.getLogger(__name__)



def home_view(request):
    logger.debug("Test log message")
    return render(request, 'base/home.html')

def test(request):
    SendEmail.user_email_verification(request.user)
    return redirect('base:home')


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
            SendEmail.user_email_verification(user)
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
