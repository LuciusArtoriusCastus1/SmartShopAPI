from django_filters.rest_framework import FilterSet, BaseInFilter, RangeFilter, CharFilter, NumberFilter

from products.models import Products


class InCharFilter(BaseInFilter, CharFilter):
    pass


class InNumberFilter(BaseInFilter, NumberFilter):
    pass


class ProductsFilter(FilterSet):
    category = InCharFilter(field_name='category__name', lookup_expr='in')
    made_in = InCharFilter(field_name='made_in__name', lookup_expr='in')
    price__gte = NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = NumberFilter(field_name='price', lookup_expr='lte')
    manufacture_year = InNumberFilter(field_name='manufacture_year__name', lookup_expr='in')
    rate__gte = NumberFilter(field_name='rate', lookup_expr='gte')
    rate__lte = NumberFilter(field_name='rate', lookup_expr='lte')

    class Meta:
        model = Products
        fields = ('category', 'made_in', 'price', 'manufacture_year', 'rate')
