
import os
import json
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


from mainapp.models import CategoryProduct, Product

JSON_PATH = 'mainapp/fixtures'


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('mainapp/fixtures/category.json')

        CategoryProduct.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = CategoryProduct(**cat)
            new_category.save()

        products = load_from_json('mainapp/fixtures/products.json')

        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = CategoryProduct.objects.get(id=category)
            prod['category'] =_category
            new_category = Product(**prod)
            new_category.save()