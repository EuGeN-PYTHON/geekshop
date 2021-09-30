import os
from django.shortcuts import render
from datetime import datetime, timedelta
# import json
from mainapp.models import Product,CategoryProduct

#
# with open('mainapp/fixtures/products.json', 'r') as f:
#     prod = json.load(f)

date = datetime.now()


# Create your views here.

def index(request):

    context = {
        'title': 'geekshop',
        'date': date
    }
    return render(request, 'mainapp/index.html', context)

def products(request):

    context = {
        'title': 'products',
        'date': date,
        'products': Product.objects.all(),
        'categories': CategoryProduct.objects.all()
    }
    return render(request, 'mainapp/products.html', context)

