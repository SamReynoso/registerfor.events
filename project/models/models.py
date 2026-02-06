from django.conf import settings
from django.db import models
import hashlib
import secrets


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile',
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        full_name = self.first_name + self.last_name
        if full_name != '':
            return full_name
        return self.user.username


class Sports(models.TextChoices):
    BASKETBALL = 'basketball', 'Basketball'
    SOCCER = 'soccer', 'Soccer'


class Gender(models.TextChoices):
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


class State(models.TextChoices):
    CALIFONIA = "calilfornia", "California"


class Cities(models.TextChoices):
    BAKERSFIELD = "bakersfield", "Bakersfield"


class Event(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    city = models.CharField(max_length=150, unique=True)
    state = models.CharField(max_length=20,
                             choices=State.choices,
                             default=State.CALIFONIA)
    sport = models.CharField(max_length=20,
                             choices=Sports.choices,
                             default=Sports.BASKETBALL)
    # start_date = models.DateField()
    # end_date = models.DateField()
    public = models.BooleanField(default=False)

    def upcoming(self):
        return True

    def status(self):
        cancelled = False
        if cancelled:
            return "Cancelled"
        if self.upcoming():
            return "Upcoming"
        return "Completed"


class Division(models.Model):
    event = models.ForeignKey(Event,
                              related_name='divisions',
                              on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=Gender.choices)
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
    name = models.CharField(max_length=150, unique=True)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    division = models.CharField(max_length=20,
                                choices=DivisionChoices.choices,)
    sport = models.CharField(max_length=20,
                             choices=Sports.choices,)


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
                             on_delete=models.CASCADE,
                             blank=True
                             )
    # canceled = model...
    # withdrawn = model...
    # attended = model...
