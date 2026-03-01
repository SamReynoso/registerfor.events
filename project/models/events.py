from models.models import Event
from invoice.models import EventRecord

class EventCRUD:
    __attr_names = (
                'name',
                'address',
                'city',
                'state',
                'sport',
                'start_date',
                )

    @staticmethod
    def __create_record(event: Event):
        record = EventRecord.objects.create(
                obj=event,
                name=event.name,
                address=event.address,
                city=event.city,
                state=event.state,
                sport=event.sport,
                start_date=event.start_date,
                )
        return record


    @staticmethod
    def __get_or_create_record(event: Event):
        try:
            record = EventCRUD.get_record(event)
            created = False
        except:
            record = EventCRUD.__create_record(event)
            created = True
        return record, created



    @staticmethod
    def __update_record(event: Event, commit=True):
        assert event.pk, f'event.pk is {event.pk}'
        record = EventCRUD.get_record(event)
        for k in EventCRUD.__attr_names:
            setattr(record, k, getattr(event, k))
        if commit:
            record.save()
        return record


    @staticmethod
    def get_record(event: Event):
        return EventRecord.objects.get(obj=event)


    @staticmethod
    def create(*args, **kwargs):
        event = Event.objects.create(*args, **kwargs)
        EventCRUD.__create_record(event)
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
        else:
            ret = event.save()
            EventCRUD.__create_record(event)
            return ret
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
