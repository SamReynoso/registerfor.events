from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from models.forms import RegisterForm
from models.models import Profile, Registration
from project.services.email import (
        send_signup_email_verification_email,
        )

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


def home_view(request):
    return render(request, 'base/home.html')


def test_view(request):
    reg = Registration.objects.all().first()
    print(reg)
    context = {'registration': reg}
    return render(request, 'email/host_new_registration_email.html', context)


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
            return redirect('user:account')
        else:
            error = 'Invalid credentials'

    return render(request, 'base/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('base:login')
