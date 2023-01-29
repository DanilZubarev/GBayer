from django.urls import path

from .views import *

urlpatterns = [
    path('', start, name='start'),
    path('general', general, name='general'),
    path('product/<int:product_id>', product, name='product'),
    path('client/<int:client_id>', client, name='client'),
    path('new_product', new_product, name='new_product'),
    path('copy_product/<int:product_id>', copy_product, name='copy_product')
]
