from models.models import Event
from invoice.models import EventRecord

import logging


logger = logging.getLogger(__name__)


class EventCRUD:
    __attr_names = (
                'name',
                'address',
                'city',
                'state',
                'sport',
                'start_date',
                'end_date',
                )

    @staticmethod
    def __create_record(event: Event):
        record = EventRecord.objects.create(
                name=event.name,
                address=event.address,
                city=event.city,
                state=event.state,
                sport=event.sport,
                start_date=event.start_date,
                end_date=event.end_date,
                )
        return record


    @staticmethod
    def __update_record(event: Event, commit=True):
        assert event.pk, f'event.pk is {event.pk}'

        for k in EventCRUD.__attr_names:
            setattr(event.record, k, getattr(event, k))
        if commit:
            event.record.save()
        return event.record



    @staticmethod
    def create(*args, **kwargs):
        event = Event(*args, **kwargs)
        record = EventCRUD.__create_record(event)
        event.record = record
        event.save()
        logger.info("Created Event", extra={"event_id": event.id})

        return event

    @staticmethod
    def update(event: Event, **kwargs):
        for k, v in kwargs.items():
            if k not in EventCRUD.__attr_names:
                raise ValueError(
                        f'{k} is not a attribute handles by {EventCRUD.__class__.__name__}'
                        )
            setattr(event, k, v)

        EventCRUD.__update_record(event)
        return event.save()


    @staticmethod
    def save(event):
        if event.pk:
            EventCRUD.__update_record(event)
            logger.info("Record updated")
        else:
            logger.info("New Event saved")
            record = EventCRUD.__create_record(event)
            event.record = record
            return event.save()
        return event.save()

    @staticmethod
    def delete(event: Event):
        event.delete()

    @staticmethod
    def open_registration(event: Event):
        event.registration_opened = True
        event.status = Event.Status.REGISTERING
        event.save()

    @staticmethod
    def close_registration(event: Event):
        event.registration_opened = False
        event.status = Event.Status.CREATED
        event.save()
        ...

    @staticmethod
    def mark_as_scheduled(event):
        event.registration_opened = False
        event.status = Event.Status.SCHEDULED
        event.save()
