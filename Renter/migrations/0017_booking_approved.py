# Generated by Django 5.1.5 on 2025-02-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Renter', '0016_review_renter_review_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='approved',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
