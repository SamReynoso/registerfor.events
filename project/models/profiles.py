from django.conf import settings
from django.contrib.auth import get_user_model
from models.models import Profile



class GetProfile:
    User = get_user_model()

    def __init__(self, user_id: int):
        user = self.User.objects.get(id=user_id)
        self.profile: Profile = user.profile

