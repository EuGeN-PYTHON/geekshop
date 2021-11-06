import os

from datetime import datetime

from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.models import Product, CategoryProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings

date = datetime.now()

MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


class IndexList(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data(**kwargs)
        context['date'] = datetime.now()
        context['title'] = 'GeekShop'
        return context






# def index(request):
#     context = {
#         'title': 'GeekShop',
#         'date': date
#     }
#     return render(request, 'mainapp/index.html', context)


class ProductList(ListView):

    template_name = 'mainapp/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_links_category(self):
        if settings.LOW_CACHE:
            key = 'links_category'
            link_category = cache.get(key)
            if link_category is None:
                link_category = CategoryProduct.objects.all()
                cache.set(key, link_category)
            return link_category
        else:
            return CategoryProduct.objects.all()

    def get_links_products(self):
        if settings.LOW_CACHE:
            key = 'links_products'
            link_produkt = cache.get(key)
            if link_produkt is None:
                link_produkt = Product.objects.all().select_related('category')
                cache.set(key, link_produkt)
            return link_produkt
        else:
            return Product.objects.all().select_related('category')


    def get_queryset(self, category_id=None, **kwargs):
        category_id = self.kwargs.get('category_id')
        if category_id != None:

            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    # @cache_page(3600)
    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['date'] = datetime.now()
        context['title'] = 'Каталог'
        context['categories'] = CategoryProduct.objects.all()
        context['products'] = self.get_queryset()
        return context

    # @staticmethod
def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    # @cache_page(3600)
    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()

        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = CategoryProduct.objects.all()
        return context

# @cache_page(3600)
# def products(request, category_id=None, page=1):
#     products1 = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
#
#     paginator = Paginator(products1, per_page=3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#
#     context = {
#         'title': 'products',
#         'date': datetime.now(),
#         'categories': CategoryProduct.objects.all(),
#         'products': products_paginator
#     }
#     return render(request, 'mainapp/products.html', context)
