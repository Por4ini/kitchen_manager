from django.urls import path
from .views import *

urlpatterns = [
    path('', bucket, name='bucket'),
    path('<str:provider>', create_order, name='create_order'),
    path('to_excel/<str:provider>', to_excel),
    path('<str:provider>/delete/<str:pk>', delete_order),
    path('<str:provider>/minus/<str:pk>', minus),
    path('<str:provider>/plus/<str:pk>', plus),
]
