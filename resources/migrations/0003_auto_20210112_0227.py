# Generated by Django 3.1.3 on 2021-01-11 20:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20210112_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='next_schedule',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 11, 21, 27, 40, 864846, tzinfo=utc)),
        ),
    ]