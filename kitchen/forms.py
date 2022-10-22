from django import forms
from .models import Order, PriceList


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('title', 'how_match', 'unit')
        widgets ={
            'title': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'how_match': forms.TextInput(attrs={'class': 'form-control'}),
        }
