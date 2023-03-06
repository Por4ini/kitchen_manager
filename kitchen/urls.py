from django.urls import path
from .views import *

urlpatterns = [
    path('', kitchen, name='kitchen'),
    path('create_request/<int:kitchens_id>/', create_request, name='create_request'),
    # path('create_request/<int:kitchens_id>/edit', edit, name='edit'),
    # path('create_request/<int:kitchens_id>/update/<str:id>', update, name='update'),
    # path('create_request/<int:kitchens_id>/delete/<str:id>', delete, name='delete'),
    path('create_request/send/<int:kitchens_id>', send_order, name='send'),
    path('create_request/<int:kitchens_id>/order/<str:date>/', order_archive),
]
