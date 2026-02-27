from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def account(request):
    return render(request, 'user/account.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'user/profile.html')
