from models.models import Event, Registration


class RegistrationOps:
    @staticmethod
    def get_event_division_keys(event: Event):
        return [ division.get_key() for division in event.divisions.all() ]

    @staticmethod
    def get_current_registration(owner, event: Event):
        return Registration.objects.filter(owner=owner, event=event).first()

    @staticmethod
    def get_registered_teams(registration):
        if registration is not None:
            if registration.items.all():
                return [item.team for item in registration.items.all()]
        return []
