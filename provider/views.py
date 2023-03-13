from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect
from kitchen.models import *
from data.utils import generate
from django.contrib.auth.hashers import make_password



def prov_list(request):
    title = "Список постачальників"
    p_user = User.objects.all()
    if request.method == 'POST':
        unique_values = set()
        providers = Provider.objects.all()
        for provider in providers:
            title = provider.title
            if '@' in title:
                values = title.split("@")
                unique_values.add(values[0].strip())
        for title in unique_values:
            query = Provider.objects.filter(title__startswith=title)
            query = query.values('title', 'email')
            mail_list = []
            for item in query:
                if item['email'] != 'None':
                    mail_list.append(item['email'])
            try:
                # Перевірка чи існує користувач з таким же значенням "first_name"
                existing_user = User.objects.get(first_name=title)
                print('Такий постачальник вже існує')
            except User.DoesNotExist:
                if mail_list:
                        provider_user = User.objects.create(first_name=title, email=mail_list[0], is_active=False,
                                                                    last_name='Provider', password='None',username=generate()[0])
                        provider_user.save()
                else:
                        provider_user = User.objects.create(first_name=title, email='Тут може бути ваша реклама!',
                                                            is_active=False, last_name='Provider', username=generate()[0],password='None')
                provider_user.save()
                print('Додано постачальника')
        return redirect('provider')


    return render(request, 'provider/index.html', {'title': title, 'p_user': p_user})

#
def activate_provider(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        provider = User.objects.get(username=username)



        password = generate()[1]
        provider.password = make_password(password)
        provider.is_active = True
        provider.save()

        try:
            email_message = EmailMessage('Дані авторизації',
                                         f'Данні для авторизації:\nLogin: {username}\nPassword: {password}',
                                         'order@kitchen-manager.com.ua',
                                         ['fert1k@icloud.com', 'p.butovets@gmail.com'])
            email_message.send()
        except Exception as e:
            return HttpResponseServerError(str(e))

        return HttpResponse("Password generated and sent to user's email")
    else:
        return render(request, 'provider/index.html')


# # 'p.butovets@gmail.com'

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Успішна реєстрація')
#             return redirect('kitchen')
#         else:
#             messages.error(request, 'Помилка реєстрації')
#     else:
#         form = UserRegisterForm()
#     form = UserRegisterForm()
#     title = 'Реєстрація'
#     return render(request, 'users/register.html', {'title':title, 'form':form})