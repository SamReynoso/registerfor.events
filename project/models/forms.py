from django import forms
from models.models import Profile, Event, Team
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'sport', 'city', 'state']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'gender', 'division', 'sport']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)
