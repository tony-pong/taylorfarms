# Generated by Django 4.2.9 on 2024-05-23 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('failures', '0002_customersku_failurerecord_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='failurerecord',
            name='submitted_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='failurerecord',
            name='date',
            field=models.DateTimeField(),
        ),
    ]