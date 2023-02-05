from django.urls import path

from .views import *

urlpatterns = [
    path('am/<slug:name>', am, name='am'),
]