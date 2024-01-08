from rest_framework import serializers

from core.models import Cart
from products.serializers import ProductsListSerializer


class CartCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ['owner']


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='display_name', read_only=True)
    product = ProductsListSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
