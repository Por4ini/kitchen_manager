from django.shortcuts import render, redirect
from data.get_api import *
from django.contrib import messages
from kitchen.models import *
from datetime import datetime


# Create your views here.

def get_req(request):
    title = 'Створеня заявки'
    if request.user.is_superuser == 1:
        data = Order.objects.all()
        a = []
        i = {}
        for item in data:
            a.append(item.kitchen.id)
        b = set(a)
        for int in b:
            for item in data:
                if int == item.kitchen.id:
                    i.update({int: item.kitchen.title})
                    break
    else:
        b = 'Ви не маєте прав на перегляд данної сторінки'
    return render(request, 'manager/index.html', {'title': title, 'b': i})


def get_order(request, id):
    o = PriceList.objects.all()

    orders = Order.objects.filter(kitchen_id=id)
    kitchen = Kitchens.objects.filter(pk=id)
    data = Order.objects.all()
    a = []
    i = {}
    for item in data:
        a.append(item.kitchen.id)
    b = set(a)
    for int in b:
        for item in data:
            if int == item.kitchen.id:
                i.update({int: item.kitchen.title})
                break

    return render(request, 'manager/order.html', {'b': i, 'orders': orders, 'kitchen': kitchen, 'o': o, })


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
                    how_match=how_match,
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
    # return redirect(request, 'manager/order.html')


def connect(request):
    title = 'Оновлення бази'
    if request.method == 'POST':
        if get_kitchen() and get_provider() == True:
            messages.success(request, 'База успішно оновлена!')
            print('true')
        else:
            messages.error(request, 'Помилка оновлення бази, зверніться до розробника.')
            print('false')

    return render(request, 'manager/connect.html', {'title': title})


def to_bucket(request, id):
    data = Order.objects.filter(kitchen_id=id)
    if request.method == 'POST':
        for item in data:
            order = Order(
                id=item.id,
                how_match=item.how_match,
                unit_id=item.unit.id,
                title_id=item.title.id,
                kitchen_id=item.kitchen.id,
                chef=item.chef,
                price_list_id=item.price_list.id,
                send=True,
                bucket=True,
            )
            order.save()
        return redirect(f'/manager/order/{id}', {'data': data})

    return redirect(f'/manager/order/{id}', {'data': data})

