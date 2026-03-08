from typing import Any


SIGNUP_EMAIL_VERIFICATION_TEMPLATE = 'email/cta.html'
SIGNUP_EMAIL_VERIFICATION: dict[str, Any] = {
        'heading': 'Welcome to Register For Events',
        'body_text': 'Thanks for signing up.',
        'cta_label': 'Verify Email',
        }


''' Event Registration '''
EVENT_REGISTRATION_TEMPLATE = 'email/registration.html'
EVENT_REGISTRATION: dict[str, Any]  = {
        'heading': 'New Registration For Event',
        'body_text': 'Registration details are listed in the table below.',
        'cta_label': 'View registration',
        }

EVENT_REGISTRATION_WITHDRAWN_TEMPLATE = 'email/registration_email.html'
EVENT_REGISTRATION_WITHDRAWN: dict[str, Any] = {
        'heading': 'Registration Withdrawn',
        'body_text': 'A registered team has withdrawn from one of your '
        'events.',
        'cta_label': 'View your event',
        }


EVENT_REGISTRATION_CANCELED_TEMPLATE = 'email/registration.html'
EVENT_REGISTRATION_CANCELED: dict[str, Any] = {
        'heading': 'Registration canceled',
        'body_text': 'The host of an event canceled your registers.',
        'cta_label': 'View event',
        }


''' Event Status '''
EVENT_CREATED_TEMPLATE = 'email/cta.html'
EVENT_CREATED: dict[str, Any]  = {
        'heading': 'Event Created',
        'body_text': 'You Created an Event.',
        'cta_label': 'View your events',
        }

EVENT_CANCELED_TEMPLATE = 'email/cta.html'
EVENT_CANCELED: dict[str, Any]  = {
        'heading': 'Event canceled',
        'body_text': 'The host of an event you where registers for has '
        'canceled the event.',
        'cta_label': 'View your events',
        }



''' RSVP '''
RSVP_TEMPLATE = 'email/rsvp.hmtl'
RSVP: dict[str, Any]  = {
        'heading': 'New RSVP',
        'body_text': 'Someone new is going to your event.',
        'cta_label': 'View event',
        }
