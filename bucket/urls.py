from django.urls import path
from .views import *

urlpatterns = [
    path('', bucket, name='bucket'),
    path('<str:id>', create_order, name='create_order'),
    path('to_excel/<str:id>', to_excel),
    path('<str:id>/delete/<str:pk>', delete_order),
    path('<str:id>/plus/<str:pk>', plus),
    path('<str:id>/minus/<str:pk>', minus),
]
