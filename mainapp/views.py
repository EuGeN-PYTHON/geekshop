import os

from django.shortcuts import render
from datetime import datetime

from mainapp.models import Product, CategoryProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

date = datetime.now()

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.

def index(request):
    context = {
        'title': 'GeekShop',
        'date': date
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    products1 = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    paginator = Paginator(products1, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)


    context = {
        'title': 'products',
        'date': date,
        'categories': CategoryProduct.objects.all(),
        'products': products_paginator
    }
    return render(request, 'mainapp/products.html', context)
