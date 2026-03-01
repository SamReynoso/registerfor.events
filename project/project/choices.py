from django.db import models


class Sports(models.TextChoices):
    BASKETBALL = 'basketball', 'Basketball'


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


class RegistrationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Canelled'
    WITHDRAWN = 'withdrawn', 'Withdrawn'
    ATTENDED = 'attended', 'Attended',


class EventStatus(models.IntegerChoices):
    CREATED = 1, "Created"
    REGISTERING = 2, "Registering"
    SCHEDULED = 3, "Scheduled"
    RUNNING = 4, "Running"
    COMPLETED = 5, "Completed"


class InvoiceStatus(models.IntegerChoices):
    DRAFT = 1, 'Draft'
    ISSUED = 2, 'Issued'
    SENT = 3, 'Sent'
    PAID = 4, 'Paid'

class InvoiceError(models.IntegerChoices):
    NONE = 1, 'None'
    MODIFIED = 2, 'Modified'
    PAST_DUE = 3, 'Past Due'
    PARTIALLY_PAID = 4, 'Partially Paid'
    VOID = 6, 'Void'
    REFUNDED = 7, 'Refunded'


class ErrorLevel(models.IntegerChoices):
    WARN = 1, 'Warn'
    ERROR = 2, 'Error'
    CRITICAL = 3, 'Critical'
