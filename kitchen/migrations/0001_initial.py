# Generated by Django 3.2.16 on 2022-10-24 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kitchens',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('technical_information', models.CharField(blank=True, db_column='Technical_Information', max_length=60, null=True)),
            ],
            options={
                'db_table': 'kitchens',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('article', models.CharField(blank=True, max_length=60, null=True)),
                ('item_title', models.CharField(blank=True, max_length=60, null=True)),
                ('unit', models.CharField(blank=True, max_length=60, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'price_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'db_table': 'product_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('code', models.CharField(blank=True, max_length=60, null=True)),
                ('email', models.CharField(blank=True, max_length=60, null=True)),
                ('have_price', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'provider',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'db_table': 'unit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('how_match', models.CharField(max_length=60, verbose_name='Кількість')),
                ('chef', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('send', models.BooleanField(default=False)),
                ('bucket', models.BooleanField(default=False)),
                ('to_prov', models.BooleanField(default=False)),
                ('kitchen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.kitchens', verbose_name='Кухні')),
                ('price_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.pricelist', verbose_name='Ціна/Постачальник')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.productlist', verbose_name='Продукт')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen.unit', verbose_name='Одиниця виміру')),
            ],
            options={
                'db_table': 'neworder',
                'managed': True,
            },
        ),
    ]
