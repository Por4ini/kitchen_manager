from django.urls import path
from .views import *

urlpatterns = [
    path('', get_req, name='request'),
    path('connect/', connect, name='connect'),
    path('order/<str:id>', get_order, name='get_order'),
    path('order/<str:id>/edit', edit_order, name='edit_order'),
    path('order/<str:id>/update/<str:pk>', update_order, name='update_order'),
    path('order/<str:id>/delete/<str:pk>', delete_order, name='delete_order'),
    path('order/send_order/<str:id>', to_bucket, name='to_bucket'),
]
