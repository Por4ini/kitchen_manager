from django.shortcuts import render, redirect
from kitchen.models import *
from datetime import datetime
import json
import pandas as pd
from platform import python_version
from django.core.mail import send_mail, EmailMessage


# Create your views here.
def bucket(request):
    title = 'Кошик'
    data = Order.objects.filter(bucket=True)
    i = []
    prov = {}
    for item in data:
        i.append(item.price_list.provider.id)
    for num in set(i):
        for item in data:
            if num == item.price_list.provider.id:
                prov.update(({num: item.price_list.provider.title}))
                break
    return render(request, 'bucket/index.html', {'title': title, 'prov': prov, 'data': data, 'my_date': datetime.now()})


def create_order(request, id):
    title = 'Кошик'
    data = Order.objects.filter(bucket=True)
    i = []
    prov = {}
    for item in data:
        i.append(item.price_list.provider.id)
    for num in set(i):
        for item in data:
            if num == item.price_list.provider.id:
                prov.update(({num: item.price_list.provider.title}))
                break
    kitchens = Kitchens.objects.all()
    k = []
    for item in data:
        for kitchen in kitchens:
            if item.kitchen_id == kitchen.id:
                k.append(kitchen.id)
    values = {}

    for item in set(i):
        if str(item) == str(id):

            total_sum = 0
            values[item] = []
            for kit in kitchens:
                sum = 0
                for order in data:

                    if order.price_list.provider_id == item and order.kitchen_id == kit.id:
                        a = float(order.price_list.price) * float(order.how_match)
                        sum += a
                    else:
                        continue
                total_sum += sum

                if sum != 0:
                    values[item].append({
                        kit.id: sum
                    })
            total_sum1 = total_sum

    return render(request, 'bucket/index.html',
                  {'kitchens': kitchens, 'kitchens_id': set(k), 'title': title, 'prov': prov, 'data': data,
                   'my_date': datetime.now(), 'id': int(id), 'values': values, 'total': total_sum1})


def to_excel(request, id):
    today = datetime.now()
    d1 = today.strftime("%d-%m-%Y")
    if request.method == "POST":

        data = Order.objects.filter(bucket=True)
        i = []

        prov = {}
        for item in data:
            i.append(item.price_list.provider.id)
        for num in set(i):
            for item in data:
                if num == item.price_list.provider.id:
                    prov.update(({num: item.price_list.provider.title}))
                    break
        kitchens = Kitchens.objects.all()
        k = []
        for item in data:
            if str(item.price_list.provider.id) == str(id):
                for kitchen in kitchens:
                    if item.kitchen_id == kitchen.id:
                        k.append(kitchen.id)

        with open('new_file.json') as json_file:
            json_data = json.load(json_file)
            json_data['id'].clear()
        json_data["id"].append({"date": d1})

        for item in set(k):
            for kit in kitchens:
                if str(item) == str(kit.id):
                    sum = 0
                    json_data["id"].append({"Підприємство ":
                        {
                            "Назва": kit.title,
                            "ФОП": kit.technical_information,
                            "Адреса": kit.address,
                        }})

                    for order in data:
                        if int(order.price_list.provider_id) == int(id) and order.kitchen_id == kit.id:
                            a = float(order.price_list.price) * float(order.how_match)
                            sum += a
                            json_data["id"].append({"Продукт ":
                                {
                                    "Найменування": order.price_list.item_title,
                                    "Кількість": order.how_match,
                                    "Одиниця виміру": order.unit.title,
                                    "Ціна, грн": float(order.price_list.price),
                                    "Сума, грн": a,
                                }})
                    if sum != 0:
                        json_data["id"].append({"Загальна сума ":
                            {
                                'Сумма': sum
                            }})
                        break

            with open('new_file.json', 'w', encoding='utf-8') as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
                outfile.close()
        print('use_send')
        with open('new_file.json', encoding='utf8') as file:
            data = json.load(file)

        data_list = data['id']

        df_m1 = pd.json_normalize(data_list, max_level=2)
        df_m1.to_excel('my_book.xlsx')
        data_delete = Order.objects.filter(bucket=True)
        for item in data_delete:
            if str(item.price_list.provider.id) == str(id):
                email_message = EmailMessage(f'Заявка. {d1}', 'Заявка в цьому файлі\n', 'kitchen_order@ukr.net', [ item.price_list.provider.email, 'fert1k@icloud.com'])
                email_message.attach_file('my_book.xlsx')
                email_message.send()
                print('excel відправлений')
                break
        for item in data_delete:
            if str(item.price_list.provider.id) == str(id):
                item.delete()


        return redirect(f'/bucket')

    return redirect(request, f'/bucket/{id}', {'my_date': datetime.now()})
