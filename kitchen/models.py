from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


order_time = timezone.now()
delivery_time = order_time + timedelta(days=1)


class Kitchens(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    technical_information = models.CharField(db_column='Technical_Information', max_length=60, blank=True, null=True)

    def _str_(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'kitchens'



class Provider(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    have_price = models.BooleanField(default=False)

    def _str_(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'provider'


class PriceList(models.Model):
    id = models.IntegerField(primary_key=True)
    article = models.CharField(max_length=60, blank=True, null=True)
    item_title = models.CharField(max_length=60, blank=True, null=True)
    unit = models.CharField(max_length=60, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.item_title}, {self.price}'

    class Meta:
        managed = False
        db_table = 'price_list'

class ProductList(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    unit = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'product_list'

class Unit(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'unit'


class Order(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    how_match = models.FloatField(verbose_name='Кількість')
    unit = models.CharField(max_length=60, verbose_name='Одиниця виміру')
    title = models.ForeignKey('ProductList', on_delete=models.CASCADE, null=True, verbose_name='Продукт')
    chef = models.CharField(max_length=100)
    date = models.DateTimeField(default=order_time)
    delivery_date = models.DateTimeField(default=delivery_time)
    price_list = models.ForeignKey('PriceList', on_delete=models.CASCADE, null=True, verbose_name='Ціна/Постачальник')
    send = models.BooleanField(default=False)
    bucket = models.BooleanField(default=False)
    to_prov = models.BooleanField(default=False)
    kitchen = models.ForeignKey('Kitchens', on_delete=models.CASCADE, null=True, verbose_name='Кухні')


    def __str__(self):
        return self.title
        
        
    def clean(self):
        # Замінюємо кому на крапку у значенні поля
        if self.how_match is not None and isinstance(self.how_match, str):
            self.how_match = self.how_match.replace(',', '.')
        super().clean()
        
        
    class Meta:
        managed = True
        db_table = 'neworder'

