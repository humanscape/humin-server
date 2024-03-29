# Generated by Django 3.2 on 2021-05-04 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20210504_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='events', to='events.rooms'),
        ),
        migrations.AlterField(
            model_name='users',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='events.events'),
        ),
    ]
