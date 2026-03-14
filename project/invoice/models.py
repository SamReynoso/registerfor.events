from django.conf import settings
from django.db import models
from models.models import Event, Registration
from project import choices

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from project.utils.project_models import on_team_delete


# class EventRecord(models.Model):
#     name = models.CharField(max_length=150)
#     address = models.CharField(max_length=150, blank=True)
#     city = models.CharField(max_length=20, choices=choices.Cities.choices)
#     state = models.CharField(max_length=20, choices=choices.States.choices)
#     sport = models.CharField(max_length=20, choices=choices.Sports.choices)
#     start_date = models.DateField()
#     end_date = models.DateField()


# class ContactRecord(models.Model):
#    first_name = models.CharField(max_length=30)
#    last_name = models.CharField(max_length=30)
#    email = models.EmailField()
#    phone = PhoneNumberField()


class Invoice(models.Model):
    Status = choices.InvoiceStatus

    id = settings.DEFAULT_AUTO_FIELD

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='invoices_issued',
                              on_delete=models.CASCADE)
    recipient  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='invoices',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    event = models.ForeignKey(Event,
                              related_name='invoices',
                              on_delete=models.CASCADE)
    registration = models.OneToOneField(Registration,
                                        on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    modified = models.BooleanField(default=False)
    status = models.IntegerField(choices=choices.InvoiceStatus.choices,
                                 default=choices.InvoiceStatus.DRAFT)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    @property
    def errors(self):
        return super().errors


class InvoiceError(models.Model):
    Errors = choices.InvoiceError
    Levels = choices.ErrorLevel

    class Meta:
        ordering = ['error']

    invoice = models.ForeignKey(Invoice, related_name='errors', on_delete=models.CASCADE)
    error = models.IntegerField(choices=choices.InvoiceError.choices)
    level = models.IntegerField(choices=choices.ErrorLevel.choices,)
