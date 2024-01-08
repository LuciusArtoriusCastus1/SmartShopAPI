from datetime import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import OrdersFilter
from .models import Orders
from .permissions import IsOwnerCustomerOrReadOnly
from .serializers import OrdersSerializer, OrdersListSerializer, OrdersUpdateSerializer, OrderDeclinedSerializer
from products.models import Products


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('total_price', 'order_date',)
    search_fields = ('product__name', 'product__description', 'product__owner__display_name', 'customer__display_name')
    filterset_class = OrdersFilter

    def create(self, request, *args, **kwargs):
        item = Products.objects.get(slug=kwargs.get('item_slug'))
        print(request.data['quantity'])

        if item.owner == request.user:
            return Response({'MESSAGE': 'CURRENT USER IS THE OWNER OF THIS PRODUCT'})

        if item.amount < int(request.data['quantity']):
            return Response({'MESSAGE': f'Max amount of products - {item.amount}'})

        serializer = self.get_serializer(data=request.data, context={'reauest': request})
        if serializer.is_valid():
            serializer.save(customer=request.user, product=item, total_price=int(request.data['quantity']) * item.price)

            item.amount -= int(request.data['quantity'])
            item.sold += int(request.data['quantity'])
            item.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get', ), detail=False, url_path='user_orders_list')
    def user_orders_list(self, request, *args, **kwargs):
        orders_list = Orders.objects.filter(Q(product__owner=request.user) | Q(customer=request.user))
        orders_list = self.filter_queryset(orders_list)
        serializer = self.get_serializer(instance=orders_list, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('put', 'get'), detail=True, url_path='product/sent/(?P<pk>[^/.]+)')
    def product_sent(self, request, *args, **kwargs):
        if self.get_object().paid_up or self.get_object().declined:
            return Response({'MESSAGE': 'Order is already terminated(paid or declined)'})

        serializer = self.get_serializer(instance=self.get_object(), data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sent=True, sent_date=datetime.now())

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('put', 'get'), detail=True, url_path='product/delivered/(?P<pk>[^/.]+)')
    def product_delivered(self, request, *args, **kwargs):
        if self.get_object().paid_up or self.get_object().declined:
            return Response({'MESSAGE': 'Order is already terminated(paid or declined)'})

        serializer = self.get_serializer(instance=self.get_object(), data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(delivered=True, delivery_date=datetime.now())

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('put', 'get'), detail=True, url_path='product/declined/(?P<pk>[^/.]+)')
    def product_declined(self, request, *args, **kwargs):
        if self.get_object().paid_up or self.get_object().declined:
            return Response({'MESSAGE': 'Order is already terminated(paid or declined)'})

        print(self.get_serializer())
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, context={'request': request}, partial=True)
        print(self.get_object().product.slug)

        item = Products.objects.get(slug=self.get_object().product.slug)

        if serializer.is_valid():
            serializer.save(declined=True, decline_date=datetime.now())

            item.amount += self.get_object().quantity
            item.sold -= self.get_object().quantity
            item.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('put', 'get'), detail=True, url_path='product/paid/(?P<pk>[^/.]+)')
    def product_paid(self, request, *args, **kwargs):
        if self.get_object().paid_up or self.get_object().declined:
            return Response({'MESSAGE': 'Order is already terminated(paid or declined)'})

        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(paid_up=True, pay_date=datetime.now())

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'user_orders_list'):
            return OrdersListSerializer
        elif self.action == 'create':
            return OrdersSerializer
        elif self.action == 'product_declined':
            return OrderDeclinedSerializer
        else:
            return OrdersUpdateSerializer

    def get_permissions(self):
        return [IsOwnerCustomerOrReadOnly()]
