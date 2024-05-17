from django.core.management.base import BaseCommand
from django.db import connection
from apps.product_evaluation.models import ProductEvaluation

class Command(BaseCommand):
    help = 'Populates the ProductEvaluation table with data from a specific table'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the ProductEvaluation table...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    "asset_description",
                    "date",
                    "result"
                FROM 
                    product_evaluation_data
                WHERE 
                    "asset_description" IS NOT NULL
                    AND "date" IS NOT NULL
                    AND "result" IS NOT NULL
                """)
            rows = cursor.fetchall()

        # Mapping the rows to the ProductEvaluation model and creating objects
        objects_to_create = [
            ProductEvaluation(
                asset_description=row[0],
                date=row[1],  # Assign datetime object directly
                result=row[2]
            ) for row in rows
        ]

        # Bulk create the objects
        ProductEvaluation.objects.bulk_create(objects_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the ProductEvaluation table'))
