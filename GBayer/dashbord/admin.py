from django.contrib import admin

from .models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'brand', 'product', 'batch', 'weight')
    list_display_links = ('description',)
    search_fields = ('id',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'weight', 'shipping', 'shipping_kg')


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Batch, BatchAdmin)
