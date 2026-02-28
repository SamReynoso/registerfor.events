from email.policy import default
from os import eventfd_read
from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from models.models import Event, Registration, RegistrationItem, Team
from project import choices
from project.utils.project_models import on_team_delete


class EventRecordManager(models.Manager):

    @classmethod
    def __event_to_kwargs(cls, event):
        return {
                'obj': event,
                'name': event.name,
                'address': event.address,
                'city': event.city,
                'state': event.state,
                'sport': event.sport,
                'start_date': event.start_date,
                'end_date': event.end_date,
                }

    def get_from_event(self, event: Event):
        return self.get(event=event)

    def create_from_event(self, event: Event):
        self.create(obj=event, **self.__event_to_kwargs(event))

    def update_from_event(self, event: Event):
        self.update(**self.__event_to_kwargs(event))



class EventRecord(models.Model):
    objects = EventRecordManager()

    obj = models.ForeignKey(Event,
                            related_name='records',
                            null=True,
                            default=None,
                            on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, choices=choices.Cities)
    state = models.CharField(max_length=20,
                             choices=choices.States.choices)
    sport = models.CharField(max_length=20,
                             choices=choices.Sports.choices)
    start_date = models.DateField()
    end_date = models.DateField()



class InvoiceManager(models.Manager):
    def get_or_create_from_objects(self, event: Event, contact):
        try:
            instance = self.get(event=event, contact=contact)
            created = False
        except self.model.DoesNotExist:
            instance = self.create(
                    owner=event.owner,
                    event=event,
                    event_name=event.name,
                    event_address=event.address,
                    event_city=event.city,
                    event_sport=event.sport,
                    event_start_date=event.start_date,
                    event_end_date=event.end_date,
                    contact=contact,
                    first_name=contact.profile.first_name,
                    last_name=contact.profile.last_name,
                    email=contact.profile.email,
                    phone=contact.profile.phone
                    )
            created = True
        return instance, created

class Invoice(models.Model):
    objects = InvoiceManager()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='invoices_issued',
                              on_delete=models.CASCADE)

    event_record = models.ForeignKey(EventRecord,
                                     related_name='invoices',
                                     on_delete=models.SET_NULL)

    status = models.IntegerField(
            choices=choices.InvoiceStatus, default=choices.InvoiceStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)
    modified = models.BooleanField(default=False)

    @property
    def event(self):
        return self.event_record.obj

    def create_from_objects(self):
        ...

    def invoice_update(self, **kwargs):
        event = kwargs.get('event', None)
        if event is not None:
            if self.event_record.obj is not None:
                self.event_record.update_from_event(event)
            else:
                self.event_record = (
                        EventRecord.objects.create_from_event(event)
                        )


class ContactRecord(models.Model):
    obj = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='contact_record',
                            null=True,
                            default=None,
                            on_delete=models.SET_DEFAULT)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField()


class RegistrationRecord(models.Model):
    obj = models.ForeignKey(Registration,
                            related_name='records',
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

