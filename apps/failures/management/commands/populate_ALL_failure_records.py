from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from apps.failures.models import AllFailureRecord


class Command(BaseCommand):
    help = 'Populates the AllFailureRecord table with failure data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the AllFailureRecord table...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    item_number_description,
                    date,
                    user_name,
                    commodity,
                    customer,
                    final_score  
                FROM 
                    shelf_life_data
                WHERE 
                    final_score IS NOT NULL
                    AND "item_number_description" IS NOT NULL
                    AND "item_number_description" <> ''
                """)
            rows = cursor.fetchall()

        records_to_create = []
        for row in rows:
            date = row[1]
            if timezone.is_naive(date):
                date = timezone.make_aware(date)

            records_to_create.append(
                AllFailureRecord(
                    item_number_description=row[0],
                    date=date,
                    user_name=row[2],
                    commodity=row[3],
                    customer=row[4],
                    final_score=row[5]
                )
            )

        AllFailureRecord.objects.bulk_create(records_to_create)

        total_records = len(records_to_create)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated the AllFailureRecord table with {total_records} records'))
