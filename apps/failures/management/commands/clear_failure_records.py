from django.core.management.base import BaseCommand
from apps.failures.models import FailureRecord


class Command(BaseCommand):
    help = 'Empties the FailureRecord table'

    def handle(self, *args, **kwargs):
        # Output the starting process
        self.stdout.write("Starting to clear the FailureRecord table...")

        # Clearing the FailureRecord table
        count = FailureRecord.objects.all().delete()

        # Output success message
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleared the FailureRecord table. {count[0]} records deleted.'))
