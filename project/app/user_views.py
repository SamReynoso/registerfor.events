from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from models.forms import ProfileAvatarForm, ProfileForm
from django.shortcuts import render, redirect

from project.utils.phonenumber import parse_phone


@login_required(login_url='/login/')
def profile_update(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['phone'] = parse_phone(data.get('phone'), 'US')
        form = ProfileForm(data, instance=request.user.profile)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('user:profile')
    else:
        next_url = request.GET.get('next')
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
            'current': request.user.profile.get_avatar_url(),
            'form': form,
            'target': 'avatar'
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


# @login_required(login_url='/login/')
# def registration_controls(request):
#     context = {}
#     return render(request, 'app/profile_registration_controls.html', context)
