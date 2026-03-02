from os import stat
from invoice.models import ContactRecord, Invoice, ItemRecord
from mailbox.models import Rsvp
from models.models import Division, Registration, RegistrationItem, Team

from project.services.email import SendEmail
# from project.utils.alerts import host_canceled_registration_alert_team_owner
# from project.services.email import send_registration_canceled_email
# from project.services.email import send_host_new_registration_email


    # TODO: 
    # Added methods for scripting later to move status to running and completed
    # Add a lock method that is time based something like below:
    # def status_lock(self):
    #     today = timezone.localdate()
    #     if today >= self.start_date:
    #         return True

import logging

logger = logging.getLogger(__name__)

class RegCRUD:

    @staticmethod
    def create(**kwargs) -> Registration:
        owner = kwargs.get('owner')
        event = kwargs.get('event')
        assert owner is not None
        assert event is not None

        contact = ContactRecord.objects.create(
                first_name=owner.profile.first_name,
                last_name=owner.profile.last_name,
                email=owner.profile.email,
                phone=owner.profile.phone,
                )

        invoice = Invoice.objects.create(
                owner=event.owner,
                event=event.record,
                contact=contact,
                )

        registration = Registration.objects.create(
                owner=owner,
                event=event,
                invoice=invoice,
                )

        logger.info("Created ContactRecord")
        logger.info("Created Invoice")
        logger.info("Created Registration")

        return registration



    @staticmethod
    def __create_item_record(**kwargs):
        team_name = kwargs.get('team_name')
        division_name = kwargs.get('division_name')
        gender = kwargs.get('gender')
        registration = kwargs.get('registration')
        team = kwargs.get('team')
        division = kwargs.get('division')
        invoice =  kwargs.get('invoice')


        if registration and invoice is None:
            invoice = registration.invoice
        if team and division is None:
            team_name = team.name
            if division_name is None:
                division_name = team.division
            if gender is None:
                gender = team.gender
        if division:
            if division_name is None:
                division_name = division.name
            if gender is None:
                gender = division.gender

        try:
            assert invoice is not None
            assert team_name is not None
            assert division_name is not None
            assert gender is not None
        except Exception as e:
            raise e

        record = ItemRecord.objects.create(
                invoice=invoice,
                team_name=team_name,
                division=division_name,
                gender=gender
                )
        return record

    @staticmethod
    def __create_item_no_save(registration: Registration,
                              team: Team,
                              division: Division) -> RegistrationItem:

        record = RegCRUD.__create_item_record(
                invoice=registration.invoice,
                team_name=team.name,
                division_name=division.name,
                gender=division.gender,
                )

        item = RegistrationItem(registration=registration,
                                team=team,
                                division=division,
                                record=record,
                                # unit_price=kwargs['unit_price'],
                                )

        return item

    @staticmethod
    def bulk_create_items(registration: Registration, teams: list[Team]):
        new_items = [
            RegCRUD.__create_item_no_save(
                registration,
                team,
                Division.objects.get(
                    event=registration.event,
                    name=team.division,
                    gender=team.gender,
                    )
                )
            for team in teams
                ]
        ret = RegistrationItem.objects.bulk_create(new_items)
        # send_host_new_registration_email(registration)
        # send_participant_new_registration_email(registration)
        RegCRUD.invalidate_invoice(registration.invoice)
        return ret



    @staticmethod
    def cancel(registration: Registration):
        ret = registration.delete()
        # host_canceled_registration_alert_team_owner(registration)
        # send_registration_canceled_email(registration)
        return ret

    @staticmethod
    def invalidate_invoice(_: Invoice):
        ...

    @staticmethod
    def rsvp_convert(rsvp: Rsvp) -> Registration:
        registration = RegCRUD.create(owner=rsvp.sender, event=rsvp.event)
        registration_items = []
        for team in rsvp.teams.all():
            record = RegCRUD.__create_item_record(registration=registration,
                                                  team=team)
            item = RegistrationItem(
                    registration=registration,
                    team=team,
                    division=Division.objects.get(
                        event=registration.event,
                        name=team.division,
                        gender=team.gender,
                        ),
                    record=record,
                    )
            registration_items.append(item)
        RegistrationItem.objects.bulk_create(registration_items)

        # send_host_new_registration_email(registration)
        # send_host_new_registration_email(registration)
        rsvp.delete()
        return registration
