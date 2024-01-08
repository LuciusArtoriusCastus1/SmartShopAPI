from django_filters.rest_framework import FilterSet, BaseInFilter, RangeFilter, CharFilter, NumberFilter, BooleanFilter
from core.models import Cart
from orders.models import Orders
from products.models import Products


class InCharFilter(BaseInFilter, CharFilter):
    pass


class InNumberFilter(BaseInFilter, NumberFilter):
    pass


class OrdersFilter(FilterSet):
    product__category = InCharFilter(field_name='product__category__name', lookup_expr='in')
    product__made_in = InCharFilter(field_name='product__made_in__name', lookup_expr='in')
    product__price__gte = NumberFilter(field_name='product__price', lookup_expr='gte')
    product__price__lte = NumberFilter(field_name='product__price', lookup_expr='lte')
    product__manufacture_year = InNumberFilter(field_name='product__manufacture_year__name', lookup_expr='in')
    product__rate__gte = NumberFilter(field_name='product__rate', lookup_expr='gte')
    product__rate__lte = NumberFilter(field_name='product__rate', lookup_expr='lte')
    sent = BooleanFilter(field_name='sent')
    delivered = BooleanFilter(field_name='delivered')
    paid_up = BooleanFilter(field_name='paid_up')
    declined = BooleanFilter(field_name='declined')

    class Meta:
        model = Orders
        fields = ('product__category', 'product__made_in', 'product__price', 'product__manufacture_year', 'product__rate', 'sent', 'delivered', 'paid_up', 'declined')
