# Generated by Django 4.0 on 2023-04-03 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0018_alter_order_date_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 3, 11, 49, 36, 736481)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 4, 11, 49, 36, 736481)),
        ),
    ]
