# Generated by Django 4.0 on 2023-05-11 00:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0020_alter_order_date_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 0, 23, 46, 287820)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 0, 23, 46, 287820)),
        ),
        migrations.AlterField(
            model_name='order',
            name='how_match',
            field=models.FloatField(verbose_name='Кількість'),
        ),
    ]
