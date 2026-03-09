from mailbox.models import Alert, Rsvp
from models.models import Event, Registration, RegistrationItem
import logging


logger = logging.getLogger(__name__)

class Alerts:
    @staticmethod
    def event_created(event: Event):
        Alert.objects.create(
                recipient=event.owner,
                type='event_created',
                title=f"Event '{event.name}' Created",
                body='New event was created.',
                # target=event.owner,
                )
        logger.info("Createtd new event alert")

    @staticmethod
    def new_registration(registration: Registration):
        Alert.objects.create(
                recipient=registration.event.owner,
                type='new_registration',
                title=f"New Event",
                body=f"A new team has registered for you event '{registration.event.name}'.",
                # target=registration.owner
                )

    @staticmethod
    def registration_withdrawn(registration: Registration):
        Alert.objects.create(
                recipient=registration.event.owner,
                type='team_withdrawn',
                title=(
                    "Registration withdrawn by "
                    f"'{registration.owner.profile.name}.'"
                    ),
                body=f"A team withdrew from your event '{registration.event.name}'." +
                f"'{registration.event.name}'",
                # target=registration.owner
                )

    @staticmethod
    def team_deleted(registration_item: RegistrationItem):
        Alert.objects.create(
                recipient=registration_item.registration.event.owner,
                type='team_withdrawn_by_deletion',
                title=f"Registration Withdrawn",
                body=f"A team in you event '{registration_item.registration.event.name}' was "
                f"deleted and has been withdrawn.",
                # target=registration.event
                )

    @staticmethod
    def rsvp_created(rsvp: Rsvp):
        Alert.objects.create(
                recipient=rsvp.event.owner,
                type='event_created',
                title=f'New RSVP',
                body=f"New RSVP for Event '{rsvp.event.name}' was created.",
                # target=event.owner,
                )
        logger.info("Createtd new event alert")

    @staticmethod
    def registration_canceled(registration: Registration):
        Alert.objects.create(
                recipient=registration.owner,
                type='host_canceled_registration',
                title="Registration canceled by host.",
                body=f"The event host of '{registration.event.name}' canceled"
                "your registration.",
                # target=registration.event.owner,
                )

    @staticmethod
    def event_canceled(registration: Registration):
        Alert.objects.create(
                recipient=registration.owner,
                type='host_canceled_event',
                title=f"Event '{registration.event.name}' Cancelled",
                body='An event you where registered to has been cancelled.'
                'Contact the host if you believe this was a mistake.',
                # target=registration.event.owner,
                )

