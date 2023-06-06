from django.shortcuts import render, redirect
from django.contrib import messages
from kitchen.models import *
from data.kitchen_update import get_kitchen
from data.provider_update import get_provider
from data.price_list_update import get_price_list

def get_req(request):
    title = 'Створеня заявки'
    if request.user.is_superuser == 1:
        data = Order.objects.filter(send=1, bucket=0).values('kitchen__id', 'kitchen__title').distinct()
        i = {item['kitchen__id']: item['kitchen__title'] for item in data}
    else:
        b = 'Ви не маєте прав на перегляд данної сторінки'
    return render(request, 'manager/index.html', {'title': title, 'b': i})


def get_order(request, id):
    data = Order.objects.filter(send=1, bucket=0).values('kitchen__id', 'kitchen__title').distinct()
    i = {item['kitchen__id']: item['kitchen__title'] for item in data}
    orders = Order.objects.filter(kitchen_id=id)
    kitchen = Kitchens.objects.filter(pk=id)
    providers = PriceList.objects.all()
    if orders.exists():
        return render(request, 'manager/order.html', {'b':i, 'orders': orders, 'o':providers, 'kitchen': kitchen,})
    else:
        return redirect('request')

def edit_order(request):
    return redirect(request, 'manager/order.html')


def update_order(request, id, pk):
    if request.method == 'POST':
        how_match = request.POST.get('how_match')
        provider = request.POST.get('provider')
        if provider == 'Змінити постачальника':
            messages.warning(request, 'Будьте уважнішим з вибором постачальника!')
            return redirect(f'/manager/order/{id}')
        else:
            this_order = Order.objects.filter(pk=pk)
            for title in this_order:
                order = Order(
                    id=title.id,
                    how_match=how_match.replace(',', '.'),
                    chef=request.user.username,
                    kitchen_id=id,
                    unit=title.unit,
                    title=title.title,
                    date=title.date,
                    send=True,
                    price_list_id=provider,

                )
                order.save()
            return redirect(f'/manager/order/{id}')
    return redirect(request, 'manager/order.html')


def delete_order(request, id, pk):
    this_order = Order.objects.filter(id=pk)
    this_order.delete()
    return redirect(f'/manager/order/{id}')


def connect(request):
    title = 'Оновлення бази'

    if request.method == 'POST':
        if get_kitchen(Kitchens) == True :
            messages.success(request, 'База підприємств оновлена!')
        else:
            messages.error(request, 'Помилка оновлення бази підприємств, зверніться до розробника.')

        if get_provider(Provider) == True:
            messages.success(request, 'База постачальників оновлена!')
        else:
            messages.error(request, 'Помилка оновлення бази постачальників, зверніться до розробника.')

        if get_price_list(Provider, PriceList, ProductList) == True:
            messages.success(request, 'База прайсів оновлена!')
        else:
            messages.error(request, 'Помилка оновлення бази прайсів, зверніться до розробника.')


    return render(request, 'manager/connect.html', {'title': title})


def to_bucket(request, id):
    data = Order.objects.filter(kitchen_id=id)
    if data.filter(send=True).exists(): # перевірка чи є записи з полем send=1
        if request.method == 'POST':
            for item in data:
                order = Order(
                    id=item.id,
                    how_match=item.how_match,
                    unit=item.unit,
                    title_id=item.title.id,
                    kitchen_id=item.kitchen.id,
                    chef=item.chef,
                    price_list_id=item.price_list.id,
                    send=True,
                    bucket=True,
                )
                order.save()
            return redirect('request')
        return render(request, 'manager/to_bucket.html', {'data': data})
    else: # якщо записів з полем send=1 немає, редірект на сторінку
        return redirect('request')
