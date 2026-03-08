from django.contrib import admin

from models.models import Event, Profile, Registration, RegistrationItem, User
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
    )



@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'event',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(RegistrationItem)
class RegistrationItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'registration',
        'team',
        # 'division',
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'start_date',
    )
