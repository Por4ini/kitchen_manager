from django.shortcuts import render, redirect
from kitchen.models import *
from datetime import datetime
import json
import pandas as pd
import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

import imp
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
        json_data["id"].append({"Дата": d1})

        for item in set(k):
            for kit in kitchens:
                if str(item) == str(kit.id):
                    sum = 0
                    json_data["id"].append({" ":
                        {
                            "Назва": kit.title,
                            "ФОП": kit.technical_information,
                            "Адреса": kit.address,
                        }})

                    for order in data:
                        if int(order.price_list.provider_id) == int(id) and order.kitchen_id == kit.id:
                            a = float(order.price_list.price) * float(order.how_match)
                            sum += a
                            json_data["id"].append({"-"
                                                    "git ":
                                {
                                    "Продукт": order.price_list.item_title,
                                    "Кількість": order.how_match,
                                    "Од. виміру": order.unit.title,
                                    "Ціна, грн": float(order.price_list.price),
                                    "Сума, грн": a,
                                }})
                    if sum != 0:
                        json_data["id"].append({"Загальна ":
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
        df_m1.to_excel('Заявка.xlsx')
        wb = openpyxl.load_workbook('Заявка.xlsx')
        sheet = wb.active
        sheet.column_dimensions['A'].width = 2
        sheet.column_dimensions['B'].width = 9
        sheet.column_dimensions['C'].width = 12
        sheet.column_dimensions['D'].width = 12
        sheet.column_dimensions['E'].width = 12
        sheet.column_dimensions['F'].width = 12
        sheet.column_dimensions['G'].width = 10
        sheet.column_dimensions['H'].width = 12
        sheet.column_dimensions['I'].width = 9
        sheet.column_dimensions['J'].width = 12
        sheet.column_dimensions['K'].width = 14
        row_count = sheet.max_row
        for i in range(1, row_count + 1):
            sheet.row_dimensions[i].height = 25



        wb.save("Заявка.xlsx")
        print('0')
        data_delete = Order.objects.filter(bucket=True)
        print('Отправляю')
        for item in data_delete:
            if str(item.price_list.provider.id) == str(id):
                email_message = EmailMessage(f'Заявка. {d1}', 'Заявка в цьому файлі\n', 'order@kitchen-manager.com.ua',
                                             ['kitchen_order@ukr.net', item.price_list.provider.email])
                email_message.attach_file('Заявка.xlsx')
                email_message.send()
                print('excel відправлений')
                break
        for item in data_delete:
            if str(item.price_list.provider_id) == str(id):
                print('1')
                item.delete()

        return redirect(f'/bucket')

    return redirect(request, f'/bucket/{id}', {'my_date': datetime.now()})


def delete_order(request, id, pk):
    this_order = Order.objects.filter(id=pk)
    this_order.delete()
    return redirect(f'/bucket/{id}')


def plus(request, id, pk):
    this_order = Order.objects.filter(id=pk)
    print(id)
    print(pk)
    for item in this_order:
        order = Order(
            id=item.id,
            how_match=float(item.how_match) + 1,
            chef=item.chef,
            kitchen_id=item.kitchen.id,
            unit=item.unit,
            title=item.title,
            price_list_id=item.price_list.id,
            send=item.send,
            bucket=item.bucket,
            to_prov=item.to_prov,
        )

        order.save()
        return redirect(f'/bucket/{id}')
    return redirect(f'/bucket/{id}')


def minus(request, id, pk):
    this_order = Order.objects.filter(id=pk)
    print(id)
    print(pk)
    for item in this_order:
        order = Order(
            id=item.id,
            how_match=float(item.how_match) - 1,
            chef=item.chef,
            kitchen_id=item.kitchen.id,
            unit=item.unit,
            title=item.title,
            price_list_id=item.price_list.id,
            send=item.send,
            bucket=item.bucket,
            to_prov=item.to_prov,
        )

        order.save()
        return redirect(f'/bucket/{id}')
    return redirect(f'/bucket/{id}')
