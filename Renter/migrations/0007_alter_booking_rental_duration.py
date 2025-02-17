# Generated by Django 5.1.5 on 2025-02-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Renter', '0006_alter_booking_rental_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='rental_duration',
            field=models.PositiveIntegerField(help_text='Duration in months', null=True),
        ),
    ]
