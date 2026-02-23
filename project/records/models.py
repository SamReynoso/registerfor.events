from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from models.models import Cities, Division, DivisionChoices, Event, Genders, Registration, Sports, States, Team


# class Activity(models.Model):
#    user = models.ForeignKey(
#        settings.AUTH_USER_MODEL,
#        on_delete=models.CASCADE,
#        related_name="feed_items",
#    )
#
#    content_type = models.ForeignKey(
#        ContentType,
#        on_delete=models.CASCADE,
#    )
#    object_id = models.PositiveBigIntegerField()
#    content_object = GenericForeignKey("content_type", "object_id")
#    verb = models.CharField(max_length=255)  # e.g. "liked", "posted", "commented"
#    created_at = models.DateTimeField(auto_now_add=True)
#
#    class Meta:
#        ordering = ["-created_at"]
#        indexes = [
#            models.Index(fields=["user", "-created_at"]),
#        ]


class RegistrationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Canelled'
    WITHDRAWN = 'withdrawn', 'Withdrawn'
    ATTENDED = 'attended', 'Attended',


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
    event_city = models.CharField(max_length=20, choices=Cities.choices)
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


class RegistrationRecordManager(models.Manager):
    def create_from_objects(self,
                            event: Event,
                            registration: Registration,
                            invoice: Invoice):
        team_name = None
        if registration.team:
            team_name = registration.team.name
        return self.create(
                owner=event.owner,
                invoice=invoice,
                registration=registration,
                division=registration.assigned_division,
                gender=registration.assigned_division.gender,
                division_name=registration.assigned_division.name,
                team=registration.team,
                team_name=team_name,
                )


class RegistrationRecord(models.Model):
    objects = RegistrationRecordManager()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name="registration_records")
    invoice = models.ForeignKey(Invoice,
                                on_delete=models.CASCADE,
                                related_name="registration_records")

    registration = models.ForeignKey(Registration,
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name="registration_records")

    division = models.ForeignKey(Division,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="registration_records")
    gender = models.CharField(max_length=20, choices=Genders.choices)
    division_name = models.CharField(max_length=20,
                                     choices=DivisionChoices.choices)

    team = models.ForeignKey(Team,
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name="registration_records")
    team_name = models.CharField(max_length=150)

    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
    )
