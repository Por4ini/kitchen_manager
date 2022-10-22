from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout

# Create your views here.

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

def user_login(request):
    title = 'Увійти'
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'title':title, 'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')