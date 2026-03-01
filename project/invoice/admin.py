from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'event',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'owner',
        'event_start_date',
        'email',
    )
    ordering = ('-created_at',)
