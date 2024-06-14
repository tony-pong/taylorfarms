from django.core.management.base import BaseCommand
from apps.failures.models import AllFailureRecord


class Command(BaseCommand):
    help = 'Empties the AllFailureRecord table'

    def handle(self, *args, **kwargs):
        # Output the starting process
        self.stdout.write("Starting to clear the FailureRecord table...")

        # Clearing the AllFailureRecord table
        count = AllFailureRecord.objects.all().delete()

        # Output success message
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleared the AllFailureRecord table. {count[0]} records deleted.'))
