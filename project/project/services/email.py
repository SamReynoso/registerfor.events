'''
Test

Email Verification              [ ]
New registration Host           [ ]
New registration Participatn    [ ]
Registration Canceled           [ ]
Registration withdrawn          [ ]
Event Canceled                  [ ]
'''

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.urls import reverse

from project.services import email_config
from models.models import Event, Registration
from mailbox.models import Announcement, Rsvp

import logging
import inspect
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class SendEmail:
    @staticmethod
    def __get_plain_text(context):
        return (
                f'{context['heading']}\n'
                '\n'
                f'{context['body_text']}\n'
                '\n'
                f'Check it here: {context['cta_url']}'
                )

    @staticmethod
    def __send(message):
        if not settings.ENABLE_EMAIL_NOTIFICATIONS:
            return
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            return response.status_code
        except Exception as e:
            raise e

    @staticmethod
    def __send_transactional(to_user: User,
                             template: str,
                             context: dict,
                             cta_viewname: str,
                             view_kwargs: dict = {},
                             ):
        relative = reverse(cta_viewname, kwargs=view_kwargs)
        context['cta_url'] = f'{settings.SITE_URL}{relative}'
        html_content = render_to_string(template, context)
        plain_text_content = SendEmail.__get_plain_text(context)
        caller = inspect.stack()[2][3]
        logger.info(f"'{caller}()' emailed {to_user.email}")

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to_user.email,
            subject=context['heading'],
            html_content=html_content,
            plain_text_content=plain_text_content,
        )
        SendEmail.__send(message)

    @staticmethod
    def user_email_verification(user: User):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        SendEmail.__send_transactional(
            to_user=user,
            template=email_config.SIGNUP_EMAIL_VERIFICATION_TEMPLATE,
            context=email_config.SIGNUP_EMAIL_VERIFICATION,
            cta_viewname='base:verify_email',
            view_kwargs={'uidb64': uid, 'token': token}
        )


    @staticmethod
    def __registration(registration: Registration, user: User):

        context = email_config.EVENT_REGISTRATION
        context['registration'] = registration

        SendEmail.__send_transactional(
            to_user=user,
            template=email_config.EVENT_REGISTRATION_TEMPLATE,
            context=context,
            cta_viewname='play:registration',
            view_kwargs={'registration_id': registration.id}
        )


    @staticmethod
    def play_registration(registration: Registration):
        SendEmail.__registration(registration, registration.owner,)


    @staticmethod
    def host_registration(registration: Registration):
        SendEmail.__registration(registration, registration.event.owner)


    @staticmethod
    def registration_canceled(registration: Registration):
        context = email_config.EVENT_REGISTRATION_CANCELED
        context['registration'] = registration

        SendEmail.__send_transactional(
            to_user=registration.owner,
            template=email_config.EVENT_REGISTRATION_CANCELED_TEMPLATE,
            context=context,
            cta_viewname='host:event',
            view_kwargs={'event_id': registration.event.id}
        )


    @staticmethod
    def registration_withdrawn(registration: Registration):

        context = email_config.EVENT_REGISTRATION_WITHDRAWN
        context['registration'] = registration

        SendEmail.__send_transactional(
            to_user=registration.event.owner,
            template=email_config.EVENT_REGISTRATION_WITHDRAWN_TEMPLATE,
            context=context,
            cta_viewname='host:event',
            view_kwargs={'event_id': registration.event.id}
        )


    @staticmethod
    def event_created(user: User, event: Event):
        context = email_config.EVENT_CREATED
        SendEmail.__send_transactional(
            to_user=user,
            template=email_config.EVENT_CREATED_TEMPLATE,
            context=context,
            cta_viewname='host:event',
            view_kwargs={'event_id': event.id}
        )
        logger.info("Emailed user about Event Creation")


    @staticmethod
    def event_canceled(user: User):
        context = email_config.EVENT_CANCELED

        SendEmail.__send_transactional(
            to_user=user,
            template=email_config.EVENT_CANCELED_TEMPLATE,
            context=context,
            cta_viewname='play:events',
        )

    @staticmethod
    def rsvp(rsvp: Rsvp): 
        context = email_config.RSVP
        context['rsvp'] = rsvp

        SendEmail.__send_transactional(
            to_user=rsvp.event.owner,
            template=email_config.RSVP_TEMPLATE,
            context=context,
            cta_viewname='explore:event',
            view_kwargs={'event_id': rsvp.event.id}
        )

    @staticmethod
    def announcement(announcements: list[Announcement]): 
        for an in announcements:
            context = {
                    'heading':  an.title,
                    'body_text': an.body,
                    'cta_label': 'RegisterFor.Events'
                    }

            SendEmail.__send_transactional(
                to_user=an.recipient,
                template='email/cta.html',
                context=context,
                cta_viewname='base:home',
            )
