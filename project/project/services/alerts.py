from mailbox.models import Alert
from models.models import Event, Registration
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
    def new_registrationel(registration: Registration):
        Alert.objects.create(
                recipient=registration.event.owner,
                type='new_registration',
                title=f"New event registration for '{registration.event.name}.'",
                body="A new team has registered for you event.",
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
                body='A team withdrew from your event ' +
                f"'{registration.event.name}'",
                # target=registration.owner
                )


    @staticmethod
    def team_deleted(registration: Registration):
        Alert.objects.create(
                recipient=registration.event.owner,
                type='team_withdrawn_by_deletion',
                title=f"A Registration withdrawn from '{registration.team.name}.'",
                body=f"A team in you event '{registration.event.name}' was "
                f"deleted and has been withdrawn.",
                # target=registration.event
                )


    @staticmethod
    def registration_canceled(registration: Registration):
        Alert.objects.create(
                recipient=registration.team.owner,
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

