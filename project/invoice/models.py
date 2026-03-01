from sys import implementation
from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models

from models.models import Event, Registration, RegistrationItem
# from project.utils.project_models import on_team_delete
from project import choices


class EventRecord(models.Model):
    obj = models.OneToOneField(Event,
                               related_name='record',
                               null=True,
                               default=None,
                               on_delete=models.SET_DEFAULT)

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, choices=choices.Cities.choices)
    state = models.CharField(max_length=20, choices=choices.States.choices)
    sport = models.CharField(max_length=20, choices=choices.Sports.choices)
    start_date = models.DateField()
    end_date = models.DateField()


class Invoice(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='invoices_issued',
                              on_delete=models.CASCADE)

    event_record = models.OneToOneField(EventRecord, on_delete=models.CASCADE)

    status = models.IntegerField(choices=choices.InvoiceStatus.choices,
                                 default=choices.InvoiceStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)
    modified = models.BooleanField(default=False)

    @property
    def event(self):
        return self.event_record.obj


class ContactRecord(models.Model):

    obj = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='contact_records',
                            null=True,
                            default=None,
                            on_delete=models.SET_DEFAULT)

    invoice = models.OneToOneField(Invoice,
                                   related_name='contact',
                                   on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField()


class RegistrationRecord(models.Model):

    obj = models.OneToOneField(Registration,
                               related_name='record',
                               null=True,
                               default=None,
                               on_delete=models.SET_DEFAULT)

    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ItemRecord(models.Model):

    obj = models.OneToOneField(RegistrationItem,
                               null=True,
                               on_delete=models.SET_NULL)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)

    team_name = models.CharField(max_length=150)
    division = models.CharField(max_length=20,
                                choices=choices.DivisionChoices.choices)
    gender = models.CharField(max_length=20, choices=choices.Genders.choices)
    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True)
