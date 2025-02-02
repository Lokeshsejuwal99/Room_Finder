# Generated by Django 5.1.5 on 2025-02-02 06:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Landlord', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='posted_on',
            new_name='posted_at',
        ),
        migrations.RemoveField(
            model_name='room',
            name='availability_status',
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='room_images/'),
        ),
        migrations.AlterField(
            model_name='room',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
