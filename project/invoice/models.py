from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from models.models import (
        Cities,
        Event,
        Sports,
        States
        )


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    SENT = "sent", "Sent"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    CANCELLED = "cancelled", "Cancelled"
    VOID = "void", "Void"
    REFUNDED = "refunded", "Refunded"


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
                              on_delete=models.CASCADE,
                              related_name="invoices_issued")

    event = models.ForeignKey(Event,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name="registration_records")
    event_name = models.CharField(max_length=150)
    event_address = models.CharField(max_length=150, blank=True)
    event_city = models.CharField(max_length=20, choices=Cities)
    event_state = models.CharField(max_length=20, choices=States.choices)
    event_sport = models.CharField(max_length=20, choices=Sports.choices)
    event_start_date = models.DateField()
    event_end_date = models.DateField()

    contact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                related_name="invoices_received")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField()

    status = models.CharField(max_length=20,
                              choices=InvoiceStatus,
                              default=InvoiceStatus.DRAFT
                              )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    pdf = models.FileField(upload_to="invoices/", null=True, blank=True)
