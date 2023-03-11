from django.urls import path

from .views import *

urlpatterns = [
    path('indicator_general', indicator_general, name='indicator_general'),

]