from django import template

from ..models import Basket

register = template.Library()

@register.filter(name='total_quantity')
def total_quantity(value, user):
    return Basket.total_quantity(user)

@register.filter(name='total_summary')
def total_summary(value, user):
    return Basket.total_summary(user)