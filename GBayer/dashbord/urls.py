from django.urls import path

from .views import *

urlpatterns = [
    path('am', am, name='am'),
    path('am_client/<int:client_id>', am_client, name='am_client'),
    path('sk', sk, name='sk'),
    path('sk_batch', sk_batch, name='sk_batch'),
    path('sk_send', sk_send, name='sk_send'),
]