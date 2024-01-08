from django_filters.rest_framework import FilterSet, BaseInFilter, RangeFilter, CharFilter, NumberFilter

from core.models import Cart
from products.models import Products


class InCharFilter(BaseInFilter, CharFilter):
    pass


class InNumberFilter(BaseInFilter, NumberFilter):
    pass


class CartFilter(FilterSet):
    product__category = InCharFilter(field_name='product__category__name', lookup_expr='in')
    product__made_in = InCharFilter(field_name='product__made_in__name', lookup_expr='in')
    product__price__gte = NumberFilter(field_name='product__price', lookup_expr='gte')
    product__price__lte = NumberFilter(field_name='product__price', lookup_expr='lte')
    product__manufacture_year = InNumberFilter(field_name='product__manufacture_year__name', lookup_expr='in')
    product__rate__gte = NumberFilter(field_name='product__rate', lookup_expr='gte')
    product__rate__lte = NumberFilter(field_name='product__rate', lookup_expr='lte')

    class Meta:
        model = Cart
        fields = ('product__category', 'product__made_in', 'product__price', 'product__manufacture_year', 'product__rate')
