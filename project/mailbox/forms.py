from django import forms
from mailbox.models import Announcement, Rsvp


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'body')


class RsvpForm(forms.ModelForm):
    class Meta:
        model = Rsvp
        fields = ['first_name', 'last_name', 'email', 'phone', 'team_name']

    first_name = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )
    last_name = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )

    team_name = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Team Name',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )
    last_name = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )

    email = forms.EmailField(
            widget=forms.TextInput(
                attrs={
                    'placeholder': 'Email',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )

    phone = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'type': 'tel',
                    'placeholder': 'Phone Number',
                    'style': "width:100%; padding:10px; \
                            border:1px solid #cccccc; border-radius:4px; \
                            font-size:14px; box-sizing:border-box;"
                    }
                )
            )
