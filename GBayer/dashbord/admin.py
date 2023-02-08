from django.contrib import admin

from .models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'brand', 'batch', 'product')
    list_display_links = ('description',)
    search_fields = ('id',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Brand, BrandAdmin)