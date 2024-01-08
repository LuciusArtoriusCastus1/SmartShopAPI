from rest_framework import serializers

from orders.models import Orders
from products.serializers import ProductsListSerializer


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('quantity', 'destination')


class OrdersListSerializer(serializers.ModelSerializer):
    product = ProductsListSerializer()

    class Meta:
        model = Orders
        fields = '__all__'


class OrdersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        read_only_fields = (
                                'product', 'customer', 'quantity', 'total_price', 'destination',
                                'order_date', 'sent', 'sent_date', 'delivered', 'delivery_date',
                                'paid_up', 'pay_date', 'declined', 'decline_date', 'decline_description'
                            )


class OrderDeclinedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('decline_description', )
