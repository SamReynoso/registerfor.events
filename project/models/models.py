from datetime import date
from django.utils import timezone

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from project.utils.alerts import (
        host_canceled_event_alert_team_owner,
        new_registrations_alert_event_owner,
        team_deleted_alert_event_owner,
        )
from project.utils.project_models import (
        # on_team_delete,
        uuid_upload_avatar,
        uuid_upload_event_poster,
        uuid_upload_team_photo
        )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile',
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
            upload_to=uuid_upload_avatar,
            blank=True,
            null=True)

    @property
    def name(self) -> str:
        full_name = self.first_name + self.last_name
        if full_name != '':
            return full_name
        return self.user.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return ''

    def __str__(self):
        return self.name


class Sports(models.TextChoices):
    BASKETBALL = 'basketball', 'Basketball'
    SOCCER = 'soccer', 'Soccer'


class Genders(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    MIXED = 'mixed', 'Mixed'


class DivisionChoices(models.TextChoices):
    U6 = "U6"
    U8 = "U8"
    U10 = "u10", "U10"
    U12 = "u12", "U12"
    U14 = "u14", "U14"
    U16 = "u16", "U16"
    U18 = "u18", "U18"
    U20 = "u20", "U20"
    ADULT = "adult", "Adult"
    MASTERS30 = "masters30", "Masters30"
    MASTERS40 = "masters40", "Masters40"
    MASTERS50 = "masters50", "Masters50"
    MASTERS60 = "masters60", "Masters60"
    MASTERS70 = "masters70", "Masters70"


class States(models.TextChoices):
    CALIFONIA = "calilfornia", "California"


class Cities(models.TextChoices):
    BAKERSFIELD = "bakersfield", "Bakersfield"


class Event(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, unique=True)
    state = models.CharField(max_length=20,
                             choices=States.choices,
                             default=States.CALIFONIA)
    sport = models.CharField(max_length=20,
                             choices=Sports.choices,
                             default=Sports.BASKETBALL)
    start_date = models.DateField()
    end_date = models.DateField()
    public = models.BooleanField(default=False)

    poster = models.ImageField(
            upload_to=uuid_upload_event_poster,
            blank=True,
            null=True)

    def status(self):
        today = timezone.localdate()
        if today < self.start_date:
            return 'Upcoming'
        if today <= self.end_date:
            return 'Running'
        return 'Completed'

    def get_poster_url(self):
        if self.poster:
            return self.poster.url
        return ''

    def delete(self, *args, **kwargs):
        for reg in self.registrations.filter(upcoming=True).all():
            host_canceled_event_alert_team_owner(reg)
        return super().delete(*args, **kwargs)


class Division(models.Model):
    event = models.ForeignKey(Event,
                              related_name='divisions',
                              on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=Genders.choices)
    name = models.CharField(max_length=20, choices=DivisionChoices.choices)

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['event', 'gender', 'name'],
                    name='unique_age_gender_combination'
                    )
                ]


class Team(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='teams',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=20, choices=Genders.choices)
    division = models.CharField(max_length=20,
                                choices=DivisionChoices.choices,)
    sport = models.CharField(max_length=20,
                             choices=Sports.choices,)
    photo = models.ImageField(
            upload_to=uuid_upload_team_photo,
            blank=True,
            null=True)

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['name', 'gender', 'division'],
                    name='unique_together_fields')
                ]

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return ''

    def delete(self, *args, **kwargs):
        print('team delete call')
        for reg in self.registrations.filter(upcoming=True).all():
            team_deleted_alert_event_owner(reg)
        return super().delete(*args, **kwargs)


class Registration(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='registrations',
                              on_delete=models.CASCADE)
    assigned_division = models.ForeignKey(Division,
                                          related_name='registrations',
                                          on_delete=models.CASCADE)
    event = models.ForeignKey(Event,
                              related_name='registrations',
                              on_delete=models.CASCADE)
    team = models.ForeignKey(Team,
                             related_name='registrations',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             )
    upcoming = models.BooleanField(default=True)

    # team_name = models...
    # canceled = models.BooleanField(default=False)
    # withdrawn = models.BooleanField(default=False)
    # attended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            new_registrations_alert_event_owner(self)
        super().save(*args, **kwargs)


class Announcement(models.Model):
    sender = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            related_name='sent_announcements')
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='announcements')
    title = models.CharField(max_length=255)
    body = models.TextField()
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient}: {self.title}"


