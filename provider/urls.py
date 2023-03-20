from django.urls import path
from .views import *

urlpatterns = [
    path('', prov_list, name='provider'),
    path('activate', activate_provider, name='activate_provider'),
    path('personal_office', personal_office, name='office')
]
