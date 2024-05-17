# Generated by Django 4.1.12 on 2023-12-13 05:12

import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_city_profile_country_profile_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=apps.users.models.avatar_with_id),
        ),
    ]
