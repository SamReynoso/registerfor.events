from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from models.forms import ProfileForm


@login_required(login_url='/login/')
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'user/profile_update.html', context)


@login_required(login_url='/login/')
def profile_picture_update(request):
    del request
    return redirect('user:profile')
