# Generated by Django 5.1.5 on 2025-02-22 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Renter', '0017_booking_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='renter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Renter.renter'),
        ),
    ]
