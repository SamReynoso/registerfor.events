'''
Test

Email Verification              [x]
New registration Host           [x]
New registration Participatn    [x]
Registration Canceled           [x]
Registration withdrawn          [x]
Event Canceled                  [x]
'''

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.urls import reverse


def send_mail(message):
    if not settings.ENABLE_EMAIL_NOTIFICATIONS:
        return
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise e


def send_transactional_email(to_user,
                             template: str,
                             context: dict,
                             cta_viewname: str,
                             view_kwargs: dict = {},
                             ):
    relative = reverse(cta_viewname, kwargs=view_kwargs)
    context['cta_url'] = f'{settings.SITE_URL}{relative}'
    html_content = render_to_string(template, context)
    plain_text_content = (
            f'{context['heading']}\n'
            '\n'
            f'{context['body_text']}\n'
            '\n'
            f'Check it here: {context['cta_url']}'
            )
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_user.email,
        subject=context['heading'],
        html_content=html_content,
        plain_text_content=plain_text_content,
    )
    send_mail(message)


def send_signup_email_verification_email(user):
    context = {
            'heading': 'Welcome to Register For Events',
            'body_text': 'Thanks for signing up.',
            'cta_label': 'Verify Email',
            }
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    send_transactional_email(
        to_user=user,
        template='email/cta.html',
        context=context,
        cta_viewname='base:verify_email',
        view_kwargs={'uidb64': uid, 'token': token}
    )


def send_new_registration_email(registration, user, heading):
    context = {
            'registration': registration,
            'heading': heading,
            'body_text': 'Registration details are listed in the table below.',
            'cta_label': 'View registration',
            }

    send_transactional_email(
        to_user=user,
        template='email/registration_email.html',
        context=context,
        cta_viewname='user:registration_details',
        view_kwargs={'registration_id': registration.id}
    )


def send_participant_new_registration_email(registration):
    send_new_registration_email(registration,
                                registration.owner,
                                'Your registration')


def send_host_new_registration_email(registration):
    send_new_registration_email(registration,
                                registration.event.owner,
                                'New registration'
                                )


def send_registration_canceled_email(registration):
    context = {
            'registration': registration,
            'heading': 'Registration canceled',
            'body_text': 'The host of an event canceled your registers.',
            'cta_label': 'View your events',
            }

    send_transactional_email(
        to_user=registration.owner,
        template='email/registration_email.html',
        context=context,
        cta_viewname='user:events'
    )


def send_registration_withdrawn_email(registration):
    context = {
            'registration': registration,
            'heading': 'Registration Withdrawn',
            'body_text': 'A registered team has withdrawn from one of your '
            'events.',
            'cta_label': 'View your event',
            }

    send_transactional_email(
        to_user=registration.event.owner,
        template='email/registration_email.html',
        context=context,
        cta_viewname='user:hosting_event',
        view_kwargs={'event_id': registration.event.id}
    )


def send_event_canceled_email(user):
    context = {
            'heading': 'Event canceled',
            'body_text': 'The host of an event you where registers for has '
            'canceled the event.',
            'cta_label': 'View your events',
            }

    send_transactional_email(
        to_user=user,
        template='email/cta.html',
        context=context,
        cta_viewname='user:events',
    )


def send_rsvp_email(rsvp):
    context = {
            'rsvp': rsvp,
            'heading': 'New RSVP',
            'body_text': 'Someone new is going to your event.',
            'cta_label': 'View event',
            }

    send_transactional_email(
        to_user=rsvp.event.owner,
        template='email/rsvp_email.html',
        context=context,
        cta_viewname='details:event',
        view_kwargs={'event_id': rsvp.event.id}
    )


# def send_announcement_email(announcement):
#    context = {
#            'heading': announcement.title,
#            'body_text': announcement.body,
#               }
#    html_content = render_to_string('email/announcemenet.html', context)
#    plain_text_content = ''
#
#    message = Mail(
#        from_email=settings.DEFAULT_FROM_EMAIL,
#        to_emails=announcement.recipient.email,
#        subject=context.get('heading'),
#        html_content=html_content,
#        plain_text_content=plain_text_content,
#    )
#    send_mail(message)
