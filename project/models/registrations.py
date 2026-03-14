from models.models import Division, Registration, RegistrationItem, Team
from invoice.models import Invoice 

import logging


logger = logging.getLogger(__name__)

class RegCRUD:

    @staticmethod
    def create(**kwargs) -> tuple[Registration, Invoice]:
        owner = kwargs.get('owner')
        event = kwargs.get('event')
        assert owner is not None
        assert event is not None

        registration = Registration.objects.create(
                owner=owner,
                event=event,
                )
        invoice = Invoice.objects.create(
                owner=event.owner,
                recipient=registration.owner,
                event=event,
                registration=registration,
                )

        logger.info("Created Registration")
        logger.info("Created Invoice")

        return registration, invoice

    @staticmethod
    def __create_item_no_save(registration: Registration,
                              invoice: Invoice,
                              team: Team,
                              division: Division) -> RegistrationItem:

        item = RegistrationItem(registration=registration,
                                invoice=invoice,
                                team=team,
                                division=division,
                                # unit_price=kwargs['unit_price'],
                                )

        return item

    @staticmethod
    def bulk_create_items(registration: Registration,
                          invoice: Invoice,
                          teams: list[Team]):
        new_items = [
            RegCRUD.__create_item_no_save(
                registration,
                invoice,
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
        RegCRUD.invalidate_invoice(registration.invoice)
        return ret



    @staticmethod
    def cancel(registration: Registration):
        ret = registration.delete()
        return ret

    @staticmethod
    def invalidate_invoice(_: Invoice):
        ...
