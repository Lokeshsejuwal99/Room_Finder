# Generated by Django 5.1.5 on 2025-03-06 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Renter', '0019_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
