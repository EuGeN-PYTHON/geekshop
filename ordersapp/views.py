# coding: utf-8
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin
from mainapp.models import Product
from ordersapp.forms import OrderItemsForm, OrderForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order
    form_class = OrderForm

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Создать заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_items.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Обновление заказ'

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop | Просмотр заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()


    return  HttpResponseRedirect(reverse('orders:list'))

def payment_result(request):
    # ik_co_id = 51237daa8f2a2d8413000000
    # ik_inv_id = 339800573
    # ik_inv_st = success
    # ik_pm_no = 1
    status = request.GET.get('ik_inv_st')
    if status == 'success':
        order_pk = request.GET.get('ik_pm_no')
        order_item = Order.objects.get(pk=order_pk)
        order_item.status = Order.PAID
        order_item.save()
    return HttpResponseRedirect(reverse('orders:list'))


def update_price(request, pk):
    if request.is_ajax():
        # product = Product.objects.get(pk=pk).select_related()
        product = Product.objects.get(pk=pk)
        if product:
            return JsonResponse({'price': product.price})

    return JsonResponse({'price': 0})
