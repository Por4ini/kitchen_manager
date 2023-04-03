from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from kitchen.models import *
from openpyxl import Workbook
from django.core.mail import send_mail, EmailMessage



def bucket(request):
    title = 'Кошик'
    data = Order.objects.filter(bucket=True, to_prov=False)
    providers = []
    # Пройтися по кожному об'єкту Order і отримати провайдера за допомогою зовнішнього ключа price_list
    for item in data:
        provider = item.price_list.provider.title.split('@')[0]
        providers.append(provider)
    return render(request, 'bucket/home.html', {'title': title, 'providers': set(providers)})


def create_order(request, provider):
    title = f'Замовлення від постачальника {provider}'
    data = Order.objects.filter(bucket=True, to_prov=False)
    providers = []
    order_ = Order.objects.filter(bucket=True, to_prov=False, send=True, price_list__provider__title__contains=provider).order_by(
        'date',
        'delivery_date').last()
    my_date = order_.date if order_ else None
    delivery_date = order_.delivery_date if order_ else None
    for item in data:
        provider_ = item.price_list.provider.title.split('@')[0]
        providers.append(provider_)

    orders = Order.objects.filter(bucket=True, to_prov=False,  price_list__provider__title__contains=provider)
    kitchens = Kitchens.objects.filter(order__bucket=True, order__to_prov=False,
                                       order__price_list__provider__title__contains=provider).distinct()
    kitchen_total = {}
    for kitchen in kitchens:
        kitchen_total[kitchen.id] = 0
        for order in orders:
            if order.kitchen.id == kitchen.id:
                kitchen_total[kitchen.id] += float(order.how_match) * float(order.price_list.price)

    # отримуємо список значень зі словника
    total_sum = sum(kitchen_total.values())
    if total_sum == 0:
        return redirect('bucket')
    return render(request, 'bucket/orders.html', {'title': title, 'providers': set(providers), 'orders': orders,
                                                  'my_date': my_date, 'delivery_date': delivery_date,
                                                  'kitchens': kitchens, 'kitchen_total': kitchen_total,
                                                  'total_sum': total_sum})


#
def to_excel(request, provider):
    order_date = Order.objects.filter(bucket=True, send=True, to_prov=False, price_list__provider__title__contains=provider).order_by(
        'date',
        'delivery_date').last()
    my_date = order_date.date if order_date else None
    delivery_date = order_date.delivery_date if order_date else None
    if request.method == "POST":
        # data = Order.objects.filter(bucket=True)
        data = Order.objects.filter(bucket=True, to_prov=False, send=True, price_list__provider__title__contains=provider)
        providers = []
        for item in data:
            provider = item.price_list.provider.title.split('@')[0]
            providers.append(provider)
        kitchens = Kitchens.objects.filter(order__bucket=True, order__to_prov=False,
                                           order__price_list__provider__title__contains=provider)

        wb = Workbook()
        ws = wb.active

        # додаємо заголовки для колонок дат
        ws.append(["Дата замовлення", "Дата доставки"])
        # додаємо значення дат
        ws.append([my_date, delivery_date])

        for kitchen in kitchens.distinct():
            print(kitchen)
            sum = 0
            # додаємо заголовки для колонок підприємства
            ws.append(["Назва", "ФОП", "Адреса"])

            # додаємо значення підприємства
            ws.append([kitchen.title, kitchen.technical_information, kitchen.address])
            # додаємо заголовки для колонок замовлення
            ws.append(["Продукт", "Кількість", "Одиниця виміру", "Ціна", "Сума"])
            # додаємо рядки замовлення
            for order in data:
                if order.kitchen.title == kitchen.title:
                    a = float(order.price_list.price) * float(order.how_match)
                    sum += a
                    ws.append([order.price_list.item_title, order.how_match, order.unit, order.price_list.price, a])
                    order.to_prov = 1
                    order.save()
                # додаємо загальну суму
            ws.append(["Загальна сума", sum])
            for column_cells in ws.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 2

            wb.save("my_orders.xlsx")
            print('Відправляю')
            user = User.objects.get(first_name=provider)

            if user.email and user.email != 'Тут може бути ваша реклама!':
                email = user.email
                email_message = EmailMessage(f'Заявка {my_date}', 'Заявка в цьому файлі\n', 'order@kitchen-manager.com.ua',
                                                     [email])
            else:
                email_message = EmailMessage(f'Заявка {my_date}', 'Заявка в цьому файлі\n',
                                             'order@kitchen-manager.com.ua',
                                             ['p.butovets@gmail.com'])
            email_message.attach_file('my_orders.xlsx')
            email_message.send()
            print('excel відправлений')



    return redirect(f'/bucket/{provider}')


def delete_order(request, provider, pk):
    this_order = Order.objects.filter(id=pk)
    this_order.delete()
    return redirect(f'/bucket/{provider}')


def plus(request, provider, pk):
    order = Order.objects.get(id=pk)
    order.how_match = float(order.how_match) + 1
    order.save()
    return redirect(f'/bucket/{provider}')


def minus(request, provider, pk):
    order = Order.objects.get(id=pk)
    order.how_match = float(order.how_match) - 1
    order.save()
    return redirect(f'/bucket/{provider}')
