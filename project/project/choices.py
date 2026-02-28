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
    CANCELED = 6, "Canceled"


class InvoiceStatus(models.IntegerChoices):
    DRAFT = 1, 'Draft'
    MODIFIED = 2, 'Modified'
    ISSUED = 3, 'Issued'
    SENT = 4, 'Sent'
    PARTIALLY_PAID = 5, 'Partially Paid'
    PAID = 6, 'Paid'
    OVERDUE = 7, 'Overdue'
    CANCELLED = 8, 'Cancelled'
    VOID = 9, 'Void'
    REFUNDED = 10, 'Refunded'


