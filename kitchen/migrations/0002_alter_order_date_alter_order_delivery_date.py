# Generated by Django 4.0 on 2023-03-07 09:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 7, 9, 43, 45, 765140, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 8, 9, 43, 45, 765290, tzinfo=utc)),
        ),
    ]