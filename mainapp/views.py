import os

from datetime import datetime

from django.template.context_processors import request
from django.views.generic import TemplateView, ListView

from mainapp.models import Product, CategoryProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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




    def get_queryset(self, category_id=None, **kwargs):
        category_id = self.kwargs.get('category_id')
        if category_id != None:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()


    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['date'] = datetime.now()
        context['title'] = 'products'
        # context['categories'] = CategoryProduct.objects.all()
        context['products'] = self.get_queryset()
        return context



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
