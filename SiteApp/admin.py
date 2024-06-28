from django.contrib import admin
from .models import *
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'exist', 'date_create')
    list_display_links = ('name', ) # Ссылочки по атрибуту
    list_editable = ('price', 'exist') # Изменение прямо из админки
    list_filter = ('exist', )
    search_fields = ('name', ) # Поиск по атрибутам, хорошо со стрингом

admin.site.register(Product, ProductAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'date_create', 'client_phone')
    list_display_links = ('order_number', )

@admin.register(OrderItem)
class orderitemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', )