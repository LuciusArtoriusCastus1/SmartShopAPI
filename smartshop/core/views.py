from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import CartFilter
from .permissions import IsOwnerOrAdmin
from .serializers import *
from products.models import Products


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('product__rate', 'post_date', 'price', 'sold')
    search_fields = ('product__name', 'product__description')
    filterset_class = CartFilter

    def create(self, request, *args, **kwargs):
        item = Products.objects.get(slug=kwargs.get('item_slug'))
        if item.owner != request.user:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(product=item)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'ERROR': 'Current user is the owner of this product'})

    @action(methods=('get',), detail=False, url_path='user_cart_list')
    def user_cart_list(self, request, *args, **kwargs):
        cart_list = Cart.objects.filter(owner=request.user)
        cart_list = self.filter_queryset(cart_list)
        serializer = self.get_serializer(instance=cart_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return CartCreateSerializer
        else:
            return CartSerializer

    def get_permissions(self):
        if self.action == 'delete':
            return [IsOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]
