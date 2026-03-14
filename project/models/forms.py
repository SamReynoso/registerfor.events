from django import forms
from models.models import Division, Profile, Event, Registration, RegistrationItem, Team
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
        fields = ['first_name', 'last_name', 'phone']


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
                "avatar": forms.FileInput()
            }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'sport', 'city', 'state', 'start_date', 'end_date']

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EventPriceForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['unit_price']


class DivisionPriceForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['unit_price']


class RegistrationPriceForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['unit_price']


class RegistrationItemPriceForm(forms.ModelForm):
    class Meta:
        model = RegistrationItem
        fields = ['unit_price']


class EventPosterForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['poster']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'gender', 'division', 'sport']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class TeamPhotoForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['photo']


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['gender', 'name']
