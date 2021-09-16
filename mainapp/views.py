import os

from django.shortcuts import render
from datetime import datetime, timedelta
import json

with open('mainapp/fixtures/products.json', 'r') as f:
    prod = json.load(f)

date = datetime.now() + timedelta(hours=3)


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
        'products': prod
    }
    return render(request, 'mainapp/products.html', context)
