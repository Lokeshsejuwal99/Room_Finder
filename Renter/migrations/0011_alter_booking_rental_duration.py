# Generated by Django 5.1.5 on 2025-02-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Renter', '0010_alter_booking_rental_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='rental_duration',
            field=models.PositiveIntegerField(default=1, help_text='Duration in months', null=True),
        ),
    ]
