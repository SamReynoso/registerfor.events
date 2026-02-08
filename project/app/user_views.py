from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from models.forms import ProfileAvatarForm, ProfileForm


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
    return render(request, 'app/profile_update.html', context)


@login_required(login_url='/login/')
def profile_delete(request):
    if request.method == 'POST':
        request.user.delete()
    return render(request, 'app/profile_delete.html')


@login_required(login_url='/login/')
def profile_avatar_update(request):
    if request.method == 'POST':
        form = ProfileAvatarForm(
                request.POST,
                request.FILES,
                instance=request.user.profile
                )
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileAvatarForm(instance=request.user.profile)
    context = {
            'current': request.user.porfile.get_avatar_url(),
            'form': form
               }
    return render(request, 'app/picture_update.html', context)


@login_required(login_url='/login/')
def profile_avatar_delete(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.avatar = None
        profile.save()
        return redirect('user:profile')
    context = {'current': profile.get_avatar_url()}
    return render(request, 'app/picture_delete.html', context)
