from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'time_create', 'client', 'shop', 'status', 'category')
    list_display_links = ('description',)
    search_fields = ('client', 'shop', 'status', 'category')
    list_editable = ('status',)
    list_filter = ('client', 'shop', 'status')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'telephone', 'name', 'adress')
    list_display_links = ('telephone',)
    search_fields = ('telephone',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class RateAdmin(admin.ModelAdmin):
        list_display = ('usd', 'eur', 'time_update')

admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rate, RateAdmin)
