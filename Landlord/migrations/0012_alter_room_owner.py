# Generated by Django 5.1.5 on 2025-02-21 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Landlord', '0011_alter_landlord_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Landlord.landlord'),
        ),
    ]
