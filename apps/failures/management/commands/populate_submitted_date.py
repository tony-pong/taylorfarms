from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.failures.models import FailureRecord
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate the submitted_date field based on the date field'

    def handle(self, *args, **kwargs):
        start_time = datetime.now()
        self.stdout.write(self.style.NOTICE('Starting population of submitted_date field...'))

        total_records = FailureRecord.objects.count()
        self.stdout.write(self.style.NOTICE(f'Total records to process: {total_records}'))

        updated_count = 0
        for index, record in enumerate(FailureRecord.objects.all(), start=1):
            if record.date:
                record.submitted_date = record.date.date()  # Extracting date part only (YYYY-MM-DD)
                record.save()
                updated_count += 1

            if index % 1000 == 0 or index == total_records:
                self.stdout.write(self.style.NOTICE(f'Processed {index} records...'))

        end_time = datetime.now()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(f'Successfully populated submitted_date field for {updated_count} records.'))
        self.stdout.write(self.style.SUCCESS(f'Total time taken: {duration}'))