from django.urls import path

from .views import *

urlpatterns = [
    path('am', am, name='am'),
    path('am_client/<int:client_id>', am_client, name='am_client'),
]