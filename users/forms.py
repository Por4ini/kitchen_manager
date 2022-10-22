from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Нікнейм користувача', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Ваш пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Підтвердити пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Повне ім'я",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Прізвище',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User

        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Нікнейм користувача', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Ваш пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
