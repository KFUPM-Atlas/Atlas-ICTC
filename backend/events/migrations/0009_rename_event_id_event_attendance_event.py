# Generated by Django 4.1.7 on 2023-03-13 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_rename_event_event_attendance_event_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_attendance',
            old_name='event_id',
            new_name='event',
        ),
    ]
