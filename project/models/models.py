from invoice.models import EventRecord, Invoice, ItemRecord
from project.services.email import send_event_canceled_email
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
from django.utils import timezone
from django.conf import settings
from django.db import models
from project import choices


class Profile(models.Model):
    id = settings.DEFAULT_AUTO_FIELD

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile',
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
            upload_to=uuid_upload_avatar,
            blank=True,
            null=True)

    def get_full_name(self) -> str:
        full_name = self.first_name + ' ' + self.last_name
        if full_name != '':
            return full_name
        return self.user.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/assets/defaults/anonymous-user.svg'

    def is_complete(self):
        if all([self.first_name, self.last_name, self.email, self.phone]):
            if settings.DEBUG:
                return True
            else:
                return self.email_confirmed
        return False

    def __str__(self):
        return self.name


class Event(models.Model):
    Status = choices.EventStatus

    id = settings.DEFAULT_AUTO_FIELD
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events',
                              on_delete=models.CASCADE)
    record = models.OneToOneField(EventRecord, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20,
                            choices=choices.Cities,
                            default=choices.Cities.BAKERSFIELD)
    state = models.CharField(max_length=20,
                             choices=choices.States.choices,
                             default=choices.States.CALIFONIA)
    sport = models.CharField(max_length=20,
                             choices=choices.Sports.choices,
                             default=choices.Sports.BASKETBALL)
    start_date = models.DateField()
    end_date = models.DateField()
    public = models.BooleanField(default=False)

    poster = models.ImageField(
            upload_to=uuid_upload_event_poster,
            blank=True,
            null=True)

    registration_opened = models.BooleanField(default=False)
    registration_closed = models.BooleanField(default=False)

    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.CREATED
    )

    def missing_invoices_count(self):
        return self.registrations.filter(invoice=None).count()

    def issued_invoice_count(self):
        return 0

    def delete(self, *args, **kwargs):
        for reg in self.registrations.filter(
                status=choices.RegistrationStatus.PENDING
                ).all():
            # host_canceled_event_alert_team_owner(reg)
            # send_event_canceled_email(reg.owner)
            ...
        return super().delete(*args, **kwargs)

    def get_poster_url(self):
        if self.poster:
            return self.poster.url
        return '/assets/defaults/event.webp'

    @property
    def registrations(self) -> models.QuerySet:
        return super().registrations

    @property
    def divisions(self) -> models.QuerySet:
        return super().divisions


class Division(models.Model):
    id = settings.DEFAULT_AUTO_FIELD

    event = models.ForeignKey(Event,
                              related_name='divisions',
                              on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=choices.Genders.choices)
    name = models.CharField(max_length=20,
                            choices=choices.DivisionChoices.choices)

    # In the create form it would be best to add "use event default"
    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)

    def get_key(self):
        return f'{self.name}-{self.gender}'

    @staticmethod
    def split_key(key):
        return key.split('-')

    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=['event', 'gender', 'name'],
                    name='unique_age_gender_combination'
                    )
                ]


class Team(models.Model):
    id = settings.DEFAULT_AUTO_FIELD

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='teams',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=20, choices=choices.Genders.choices)
    division = models.CharField(max_length=20,
                                choices=choices.DivisionChoices.choices,)
    sport = models.CharField(max_length=20,
                             choices=choices.Sports.choices,)
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
        return self.owner.profile.get_avatar_url()

    def get_key(self):
        return f'{self.division}-{self.gender}'

    def delete(self, *args, **kwargs):
        for reg in self.registrations.filter(upcoming=True).all():
            team_deleted_alert_event_owner(reg)
        return super().delete(*args, **kwargs)



class Registration(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="registration_records",
                              on_delete=models.CASCADE)
    event = models.ForeignKey(Event,
                              related_name='registrations',
                              on_delete=models.CASCADE)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)

    id = settings.DEFAULT_AUTO_FIELD

    status = models.CharField(
        max_length=20,
        choices=choices.RegistrationStatus.choices,
        default=choices.RegistrationStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def contact_name(self):
        return self.owner.profile.get_full_name()

    @property
    def contact_email(self):
        return self.owner.profile.email

    @property
    def contact_phone(self):
        return self.owner.profile.phone

    @property
    def contact_profile(self):
        return self.owner.profile


class RegistrationItem(models.Model):
    id = settings.DEFAULT_AUTO_FIELD

    registration = models.ForeignKey(Registration,
                                     related_name='items',
                                     on_delete=models.CASCADE)
    team = models.ForeignKey(Team,
                             related_name='items',
                             on_delete=models.CASCADE)
    division = models.ForeignKey(Division,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    record = models.OneToOneField(ItemRecord, on_delete=models.CASCADE)


    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    @property
    def invoice(self):
        return self.registration.invoice

    @property
    def contact_name(self):
        return self.registration.owner.profile.get_full_name()

    @property
    def contact_email(self):
        return self.registration.owner.profile.email

    @property
    def contact_phone(self):
        return self.registration.owner.profile.phone
