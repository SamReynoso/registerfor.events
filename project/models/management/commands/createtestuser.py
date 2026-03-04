from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from models.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser along with a profile"

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        username = options["username"]
        password = options["password"]

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("User already exists"))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        Profile.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS("Superuser and profile created successfully"))
