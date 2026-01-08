from django.contrib import admin

# Register your models here.
from .models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'assigned_staff')
    list_filter = ('category','assigned_staff')
    search_fields = ('name',)
admin.site.register(Product, ProductAdmin)