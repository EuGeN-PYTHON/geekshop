from django.views.decorators.cache import cache_page

from baskets.models import Basket
from mainapp.models import Product, CategoryProduct
from ordersapp.models import Order

#
def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user=request.user).select_related()
    return {
        'baskets': baskets_list,
    }
#
# def total_quantity_baskets(request):
#     return basket(request)['baskets'].quantity


def product(request):
    products_list = Product.objects.all().select_related()
    return {
        'products': products_list,
    }


def category(request):
    categories_list = CategoryProduct.objects.all().select_related()
    return {
        'categories': categories_list,
    }
#
# def order(request):
#     order_list = Order.objects.all().select_related()
#     return {
#         'orders': order_list,
#     }