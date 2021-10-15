
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from geekshop.mixin import CustomAuthMixin
from mainapp.models import Product
from baskets.models import Basket


# Create your views here.


# class JSONResponseMixin(object):
#     def render_to_response(self, context):
#         return self.get_json_response(self.convert_context_to_json(context))
#
#     def get_json_response(self, content, **httpresponse_kwargs):
#         return http.HttpResponse(content,
#                                  content_type='application/json',
#                                  **httpresponse_kwargs)
#
#     def convert_context_to_json(self, context):
#         return json.dumps(context)


class BasketAdd(CustomAuthMixin):
    model = Basket

    def get(self, request, *args, **kwargs):
        # if request.is_ajax():
            user_select = request.user
            product = Product.objects.get(id=self.kwargs['product_id'])
            baskets = Basket.objects.filter(user=user_select, product=product)
            if not baskets.exists():
                Basket.objects.create(user=user_select, product=product, quantity=1)
            else:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def basket_add(request, product_id):
#     user_select = request.user
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=user_select, product=product)
#     if not baskets.exists():
#         Basket.objects.create(user=user_select, product=product, quantity=1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class BasketEdit(CustomAuthMixin):
    model = Basket

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            basket = Basket.objects.get(id=self.kwargs['id'])
            if self.kwargs['quantity'] > 0:
                basket.quantity = self.kwargs['quantity']
                basket.save()
            else:
                basket.delete()

            baskets = Basket.objects.filter(user=request.user)
            context = {
                'baskets': baskets
            }
            result = render_to_string('baskets/baskets.html', context)
            return JsonResponse({'result': result})


# @login_required
# def basket_edit(request, id, quantity):
#     if request.is_ajax():
#         basket = Basket.objects.get(id=id)
#         if quantity > 0:
#             basket.quantity = quantity
#             basket.save()
#         else:
#             basket.delete()
#
#         baskets = Basket.objects.filter(user=request.user)
#         context = {
#             'baskets': baskets
#         }
#         result = render_to_string('baskets/baskets.html', context)
#         return JsonResponse({'result': result})


class RemoveBasket(CustomAuthMixin):
    model = Basket

    def get(self, request, **kwargs):
        basket_id = self.kwargs['pk']
        Basket.objects.get(id=basket_id).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required
# def basket_remove(request, basket_id):
#     Basket.objects.get(id=basket_id).delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
