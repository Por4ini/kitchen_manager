from django.urls import path
from .views import *

urlpatterns = [
    path('', bucket, name='bucket'),
    path('<str:id>', create_order, name='create_order'),
    path('to_excel/<str:id>', to_excel)
]
