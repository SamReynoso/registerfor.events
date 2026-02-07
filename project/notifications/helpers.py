from models.models import Profile
from notifications.models import Alerts


def create_alert(recipient: Profile, title: str, body: str):
    alert = Alerts.objects.create(recipient=recipient, title=title, body=body)
