
from django.db import models

from users.models import User
from mainapp.models import Product


# Create your models here.

def total_quantity(quantities=0):
    return quantities


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @property
    def get_baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_summary(self):
        return sum(item.sum() for item in self.get_baskets)

    def total_quantity(self):
        return sum(item.quantity for item in self.get_baskets)