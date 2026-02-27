from mailbox.models import Alert


def new_registrations_alert_event_owner(registration):
    Alert.objects.create(
            recipient=registration.event.owner,
            type='new_registration',
            title=f"New event registration for '{registration.event.name}.'",
            body="A new team has registered for you event.",
            # target=registration.owner
            )


def registration_withdrawn_alert_event_owner(registration):
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


def team_deleted_alert_event_owner(registration):
    Alert.objects.create(
            recipient=registration.event.owner,
            type='team_withdrawn_by_deletion',
            title=f"A Registration withdrawn from '{registration.team.name}.'",
            body=f"A team in you event '{registration.event.name}' was "
            f"deleted and has been withdrawn.",
            # target=registration.event
            )


def host_canceled_registration_alert_team_owner(registration):
    Alert.objects.create(
            recipient=registration.team.owner,
            type='host_canceled_registration',
            title="Registration canceled by host.",
            body=f"The event host of '{registration.event.name}' canceled"
            "your registration.",
            # target=registration.event.owner,
            )


def host_canceled_event_alert_team_owner(registration):
    Alert.objects.create(
            recipient=registration.owner,
            type='host_canceled_event',
            title=f"Event '{registration.event.name}' Cancelled",
            body='An event you where registered to has been cancelled.'
            'Contact the host if you believe this was a mistake.',
            # target=registration.event.owner,
            )
