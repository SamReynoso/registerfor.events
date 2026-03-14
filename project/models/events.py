from models.models import Event

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
    def create(*args, **kwargs):
        event = Event(*args, **kwargs)
        event.save()
        logger.info("Created Event", extra={"event_id": event.id})

        return event

    @staticmethod
    def update(event: Event, **kwargs):
        for k, v in kwargs.items():
            if k not in EventCRUD.__attr_names:
                raise ValueError(
                        f'{k} is not a attribute handles by '
                        f'{EventCRUD.__class__.__name__}'
                        )
            setattr(event, k, v)
        return event.save()


    @staticmethod
    def save(event):
        if event.pk:
            logger.info("Record Updated")
        else:
            logger.info("New Event Created")
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
