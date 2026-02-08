import os
import uuid

from django.db import models

from project.utils.alerts import team_deleted_alert_event_owner


def on_team_delete(collector, field, sub_objs, using):
    sub_objs.filter(
            canceled=False,
            withdrawn=False,
            attended=False
            ).update(withdrawn=True)
    upcoming = sub_objs.filter(upcoming=True)
    upcoming.update(upcoming=False)
    for reg in upcoming:
        team_deleted_alert_event_owner(reg)
    models.SET_NULL(collector, field, sub_objs, using)


def uuid_upload_avatar(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/profile/{uuid.uuid4()}{ext}"


def uuid_upload_event_poster(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/events/{uuid.uuid4()}{ext}"


def uuid_upload_team_photo(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/teams/{uuid.uuid4()}{ext}"
