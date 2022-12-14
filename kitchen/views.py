from django.shortcuts import render, redirect
import sqlite3
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, time


# Create your views here.

def index(request):
    title = 'Головна сторінка'
    return render(request, 'kitchen/index.html', {'title': title})


def kitchen(request):
    title = 'Кухні'
    kitchen = Kitchens.objects.all()
    return render(request, 'kitchen/kitchen.html', {'title': title, 'kitchen': kitchen})


def create_request(request, kitchens_id):
    title = 'Створити заявку'
    time_start = time(00)
    time_end = time(23,59)
    time_end_edit = time(23,59)
    timer = {
        'start':time_start,
        'end':time_end,
        'end_edit':time_end_edit,
    }
    kitchen = Kitchens.objects.filter(id=kitchens_id)
    data = Order.objects.filter(kitchen_id=kitchens_id)
    for item in kitchen:

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.chef = request.user.first_name + " " + request.user.last_name
                instance.kitchen_id = item.id
                instance.save()
        else:
            form = OrderForm()
    return render(request, 'kitchen/create_request.html',
                  {'time':timer, 'title': title, 'form': form, 'kitchen': kitchen,'kitchens_id':kitchens_id, 'data': data, 'my_date': datetime.now()})


def edit(request, kitchens_id):
    data = Order.objects.filter(kitchen_id=kitchens_id)

    return redirect(request, 'kitchen/create_request.html', {'data': data})


def update(request, kitchens_id, id):
    if request.method == 'POST':
        how_match = request.POST.get('how_match')
        kitchens = Kitchens.objects.filter(id=kitchens_id)
        this_order = Order.objects.filter(pk=id)
        for title in this_order:
            order = Order(
                id=id,
                how_match=how_match,
                chef=request.user.first_name + " " +  request.user.last_name,
                kitchen_id=title.kitchen.id,
                unit=title.unit,
                title=title.title
            )

            order.save()
        return redirect(f'/kitchen/create_request/{kitchens_id}')
    return redirect(request, f'/kitchen/create_request/{kitchens_id}')


def delete(request, id, kitchens_id):
    kitchens = Kitchens.objects.filter(id=kitchens_id)
    for item in kitchens:
        kitchens_id = item.id
        data = Order.objects.filter(id=id)
        data.delete()
        return redirect(f'/kitchen/create_request/{kitchens_id}')
    return redirect(request, f'/kitchen/create_request/{kitchens_id}')


def send_order(request, kitchens_id):
    print('Its okey')

    data = Order.objects.filter(kitchen_id=kitchens_id)
    if request.method == 'POST':

        for item in data:
            price = PriceList.objects.filter(item_title=item.title.title)
            a = []
            price_id = []
            for ti in price:
                if float(ti.price) == 0.0:
                    print('Нахуй')
                else:
                    a.append(float(ti.price))
            a = min(a)
            for i in price:
                if str(a) in str(i.price):
                    price_id.append(i.id)

            order = Order(
                id=item.id,
                how_match=item.how_match,
                chef=item.chef,
                kitchen_id=item.kitchen.id,
                unit_id=item.unit.id,
                title_id=item.title.id,
                send=True,
                price_list_id=price_id[0],
                bucket=item.bucket,
            )
            order.save()
        return redirect(f'/kitchen/create_request/{kitchens_id}', {'data': data})
    return redirect(f'/kitchen/create_request/{kitchens_id}', {'data': data})
