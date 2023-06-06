from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime, time
import pytz



def index(request):
    title = 'Головна сторінка'
    return render(request, 'kitchen/index.html', {'title': title})


def kitchen(request):
    title = 'Кухні'
    kitchen = Kitchens.objects.all()
    return render(request, 'kitchen/kitchen.html', {'title': title, 'kitchen': kitchen})

def create_request(request, kitchens_id):
    title = 'Створити заявку'
    kitchen = Kitchens.objects.get(pk=kitchens_id)
    title_kitchen = kitchen.title
    orders = Order.objects.filter(kitchen_id=kitchens_id)
    dates = Order.objects.filter(kitchen_id=kitchens_id).values_list('date', flat=True).distinct().order_by('date')
    unique_dates = list(set([datetime.strftime(date, '%Y-%m-%d') for date in dates]))
    unique_dates.sort()
    product_list = ProductList.objects.all()
    my_date = datetime.now(tz=pytz.timezone('Europe/Kiev'))
    if request.method == 'POST':
        for product in product_list:
            how_match = request.POST.get(product.title)
            if how_match != '0':
                how_match = how_match
                product = ProductList.objects.get(title=product.title)
                Order.objects.create(
                    how_match=how_match.replace(',', '.'),
                    unit=product.unit,
                    title_id=product.id,
                    chef= request.user.first_name + " " + request.user.last_name,
                    kitchen_id=kitchens_id
                )

        return redirect(f'/kitchen/create_request/{kitchens_id}')

    return render(request, 'kitchen/create_request.html',
                      {'unique_dates': unique_dates, 'my_date':my_date, 'title': title, 'kitchens_id': kitchens_id, 'orders': orders,'product_list':product_list, 'title_kitchen':title_kitchen})

def order_archive(request, kitchens_id, date):
    orders = Order.objects.filter(kitchen_id=kitchens_id)
    title = 'Архів замовлень'
    kitchen = Kitchens.objects.get(pk=kitchens_id)
    title_kitchen = kitchen.title
    filter_date = datetime.strptime(date, '%Y-%m-%d')
    return render(request, 'kitchen/order.html',
                  {'title': title, 'kitchens_id': kitchens_id,
                   'orders': orders, 'filter_date': filter_date, 'title_kitchen':title_kitchen})


def send_order(request, kitchens_id):
    print('Its okey')

    data = Order.objects.filter(kitchen_id=kitchens_id)
    if request.method == 'POST':

        for item in data:
            price = PriceList.objects.filter(item_title=item.title.title).exclude(price=0)
            sorted_bananas = price.order_by('price')
            cheapest_banana = sorted_bananas.first()
            price_id = cheapest_banana.id

            order = Order(
                id=item.id,
                how_match=item.how_match,
                chef=item.chef,
                kitchen_id=item.kitchen.id,
                unit=item.unit,
                title_id=item.title.id,
                send=True,
                price_list_id=price_id,
                bucket=item.bucket,
            )
            order.save()
        return redirect(f'/kitchen/create_request/{kitchens_id}', {'data': data})
    return redirect(f'/kitchen/create_request/{kitchens_id}', {'data': data})
