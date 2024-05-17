from django.core.management.base import BaseCommand
from django.db import connection
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

        FailureRecord.objects.bulk_create([
            FailureRecord(
                item_number_description=row[0],
                date=row[1],
                user_name=row[2],
                commodity=row[3],
                customer=row[4]# Adjust as per your actual data structure
            ) for row in rows
        ])

        self.stdout.write(self.style.SUCCESS('Successfully populated the FailureRecord table'))
