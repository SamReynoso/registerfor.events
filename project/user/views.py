from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mailbox.models import Alert


@login_required(login_url='/login/')
def account(request):
    context = {
            'alerts': Alert.objects.filter(recipient=request.user).all(),
            }
    return render(request, 'user/account.html', context)


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'user/profile.html')
