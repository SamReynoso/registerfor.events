import os
import uuid


def uuid_upload_avatar(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/profile/{uuid.uuid4()}{ext}"


def uuid_upload_event_poster(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/events/{uuid.uuid4()}{ext}"


def uuid_upload_team_photo(_, filename):
    ext = os.path.splitext(filename)[1]
    return f"uploads/teams/{uuid.uuid4()}{ext}"
