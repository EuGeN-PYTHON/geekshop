from django.contrib import admin
from mainapp.models import Product, CategoryProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(CategoryProduct)