from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from apps.failures.models import FailureRecord

class Command(BaseCommand):
    help = 'Populates the FailureRecord table with failure data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the FailureRecord table...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    item_number_description,
                    date,
                    user_name,
                    commodity,
                    customer  
                FROM 
                    shelf_life_data
                WHERE 
                    final_score IN ('Gross Failure', 'Failure')
                    AND "item_number_description" IS NOT NULL
                    AND "item_number_description" <> ''
                """)
            rows = cursor.fetchall()

        # Convert each row's date to a timezone-aware datetime object if it's naive
        records_to_create = []
        for row in rows:
            date = row[1]
            if timezone.is_naive(date):
                date = timezone.make_aware(date)

            records_to_create.append(
                FailureRecord(
                    item_number_description=row[0],
                    date=date,
                    user_name=row[2],
                    commodity=row[3],
                    customer=row[4]
                )
            )

        FailureRecord.objects.bulk_create(records_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the FailureRecord table'))
