# Generated by Django 3.2.4 on 2021-06-21 05:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fire_alert_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 6, 21, 5, 13, 27, 801219, tzinfo=utc)),
            preserve_default=False,
        ),
    ]