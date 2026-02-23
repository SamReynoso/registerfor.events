from django.contrib import admin
from .models import Invoice, RegistrationRecord


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'event',
        'event_name',
        'event_city',
        'event_start_date',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'first_name',
        'last_name',
        'event_start_date',
        'email',
    )
    ordering = ('-created_at',)


@admin.register(RegistrationRecord)
class RegistrationRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'first_name',
        'last_name',
        'email',
    )
    ordering = ('-created_at',)
