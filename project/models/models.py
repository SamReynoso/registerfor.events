from invoice.models import Invoice, InvoiceItem
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

    @property
    def name(self) -> str:
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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='events',
                              on_delete=models.CASCADE)
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

    def get_status(self):
        if self.status == self.Status.CANCELED:
            return self.Status.CANCELED

        status = self.Status.CREATED
        today = timezone.localdate()
        if today > self.end_date:
            status = self.Status.COMPLETED
        if today >= self.start_date and today <= self.end_date:
            status = self.Status.RUNNING

        if today < self.start_date:
            status = self.Status.CREATED
            if self.registration_opened:
                status = self.Status.REGISTERING
                if self.registration_closed:
                    status = self.Status.SCHEDULED

        self.status = status
        self.save()
        return status

    def open_registration(self):
        self.registration_opened = True
        self.status = self.Status.REGISTERING
        self.save()

    def close_registration(self):
        self.registration_opened = False
        self.status = self.Status.CREATED
        self.save()

    def mark_as_scheduled(self):
        self.registration_opened = False
        self.status = self.Status.SCHEDULED
        self.save()

    def missing_invoices_count(self):
        return self.registrations.filter(invoice=None).count()

    def issued_invoice_count(self):
        return self.registrations.filter(
                invoice__status__gt=choices.InvoiceStatus.MODIFIED
                ).count()

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


class Division(models.Model):
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


class RegistrationManager(models.Manager):
    def create_from_objects(self, owner, event: Event,):
        return self.create(
                owner=owner,
                event=event,

                first_name=owner.profile.first_name,
                last_name=owner.profile.last_name,
                email=owner.profile.email,
                phone=owner.profile.phone,
                )


class Registration(models.Model):
    objects = RegistrationManager()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="registration_records",
                              on_delete=models.CASCADE)

    event = models.ForeignKey(Event,
                              related_name='registrations',
                              on_delete=models.CASCADE)

    invoice = models.ForeignKey('invoice.invoice',
                                related_name='invoice',
                                on_delete=models.CASCADE)
#                                null=True,
#                                blank=True,
#                                on_delete=models.SET_NULL)

    status = models.CharField(
        max_length=20,
        choices=choices.RegistrationStatus.choices,
        default=choices.RegistrationStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def contact_name(self):
        if self.owner:
            return self.owner.profile.name
        return self.first_name + ' ' + self.last_name

    @property
    def teams(self):
        return [item.team for item in self.items.all() if item.team]

    def save(self, *args, **kwargs):
        if self.pk is None:
            new_registrations_alert_event_owner(self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.invoice:
            self.invoice.status = choices.InvoiceStatus.WI
        return super().delete(*args, **kwargs)


class RegistrationItem(models.Model):

    registration = models.ForeignKey(Registration,
                                     related_name='items',
                                     on_delete=models.CASCADE)
    team = models.ForeignKey(Team,
                             related_name='items',
                             on_delete=models.CASCADE)
#                             blank=True,
#                             null=True,
#                             on_delete=models.SET_NULL)
    invoice_item = models.ForeignKey(InvoiceItem,
                               related_name='registration_items',
                               on_delete=models.CASCADE)
    division = models.ForeignKey(Division,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)

    @property
    def invoice(self):
        return self.registration.invoice

