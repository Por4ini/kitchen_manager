# Generated by Django 4.0 on 2023-03-08 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0009_alter_order_date_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 8, 13, 58, 12, 603488)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 9, 13, 58, 12, 603488)),
        ),
    ]
