from django.core.management.base import BaseCommand
from django.db import connection
from apps.failures.models import GrossFailure

class Command(BaseCommand):
    help = 'Populates the gross_failure table with relevant data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the gross_failure table...")
        with connection.cursor() as cursor:
            cursor.execute("""
           SELECT 
    "item_number_description",
    COUNT(*) AS failure_count,
    TO_TIMESTAMP(
        (EXTRACT(EPOCH FROM MIN("date")) + EXTRACT(EPOCH FROM MAX("date"))) / 2
    )::date AS "date midpoint",  -- Calculating the midpoint of the dates using timestamp and casting it to date
    (
        SELECT "user_name" FROM shelf_life_data s2
        WHERE s2."item_number_description" = s1."item_number_description"
          AND s2."final_score" IN ('Gross Failure', 'Failure')
        GROUP BY "user_name"
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) AS "User"  -- Subquery to find the most common user_name
FROM 
    shelf_life_data s1
WHERE 
    "final_score" IN ('Gross Failure', 'Failure')  -- Filtering for either 'Gross Failure' or 'Failure'
    AND "item_number_description" IS NOT NULL
    AND "item_number_description" <> ''
GROUP BY
    "item_number_description"
ORDER BY 
    failure_count DESC,
    "item_number_description" ASC;

            """)
            rows = cursor.fetchall()

        for row in rows:
            GrossFailure.objects.create(
                item_number_description=row[0],
                failure_count=row[1],
                date_midpoint=row[2],
                user_name=row[3]
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the gross_failure table'))
