# Generated by Django 4.2.9 on 2024-06-13 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('failures', '0004_allfailurerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='allfailurerecord',
            name='final_score',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
