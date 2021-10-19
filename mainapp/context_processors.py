from baskets.models import Basket
from mainapp.models import Product, CategoryProduct


def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user=request.user)
    return {
        'baskets': baskets_list,
    }

def product(request):
    products_list = Product.objects.all()
    return {
        'products': products_list,
    }

def category(request):
    categories_list = CategoryProduct.objects.all()
    return {
        'categories': categories_list,
    }
