# Generated by Django 3.2 on 2021-05-03 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_events_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='calendar_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
