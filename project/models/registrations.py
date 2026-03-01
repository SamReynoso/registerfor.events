from invoice.models import ContactRecord, Invoice, ItemRecord
from mailbox.models import Rsvp
from models.models import Registration, RegistrationItem, Team
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


class RegCRUD:

    @staticmethod
    def create(**kwargs):
        owner = kwargs.get('owner')
        event = kwargs.get('event')
        assert owner is not None
        assert event is not None

        registration = Registration.objects.create(
                owner=owner,
                event=event
                )
        invoice = Invoice.objects.create(
                owner=event.owner,
                event_record=event.record
                )
        ContactRecord.objects.create(
                obj=owner,
                invoice=invoice,
                first_name=owner.profile.first_name,
                last_name=owner.profile.last_name
                )
        return registration



    @staticmethod
    def cancel(registration):
        ret = registration.delete()
        # host_canceled_registration_alert_team_owner(registration)
        # send_registration_canceled_email(registration)
        return ret

    @staticmethod
    def rsvp_convert(rsvp: Rsvp):
        registration = RegCRUD.create(owner=rsvp.sender, event=rsvp.event)
        for division in rsvp.divisions.all():
            item = RegistrationItem.objects.create(
                    registration=registration,
                    team=Team.objects.get(
                        owner=registration.owner,
                        division=division.name,
                        gender=division.gender
                        ),
                    division=division,
                    )
            ItemRecord.objects.create(
                    obj=item,
                    invoice=registration.invoice,
                    team_name=item.team.name,
                    division=item.division.name,
                    gender=item.division.gender
                    )


        # send_host_new_registration_email(registration)
        # send_host_new_registration_email(registration)
        rsvp.delete()
