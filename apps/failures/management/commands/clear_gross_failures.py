from django.core.management.base import BaseCommand
from apps.failures.models import GrossFailure


class Command(BaseCommand):
    help = 'Empties the GrossFailure table'

    def handle(self, *args, **kwargs):
        # Informing the start of the process
        self.stdout.write("Starting to clear the GrossFailure table...")

        # Performing the delete operation
        count = GrossFailure.objects.all().delete()

        # Outputting the result
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleared the GrossFailure table. {count[0]} records deleted.'))
