from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from models.models import Event


class Command(BaseCommand):
    help = "Seed the database with dummy events"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of events to create",
        )

    def handle(self, *args, **options):
        count = options["count"]

        now = timezone.now()
        start_date = now - timedelta(days=365)
        end_date = now + timedelta(days=365)

        posts = [
            Event(
                owner_id=1,
                name=f'Event {i}',
                city='bakersfield',
                state='california',
                sport='basketball',
                start_date=start_date,
                end_date=end_date,
            )
            for i in range(count)
        ]

        Event.objects.bulk_create(posts)

        self.stdout.write(self.style.SUCCESS(f"Created {count} events."))
