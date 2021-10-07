from django.contrib import admin
from mainapp.models import Product, CategoryProduct

# Register your models here.

# admin.site.register(Product)
admin.site.register(CategoryProduct)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', ('price', 'quantity', 'category'))
    readonly_fields = ('description',)
    ordering = ('name', 'price', 'quantity', 'category',)
    search_fields = ('name',)