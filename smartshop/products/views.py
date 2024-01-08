from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .filters import ProductsFilter
from .permissions import IsOwnerOrAdmin, IsSeller, IsAttachOwnerOrAdmin
from .serializers import *
from .models import Products, Rating


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    lookup_field = "slug"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('rate', 'post_date', 'price', 'sold')
    search_fields = ('name', 'description')
    filterset_class = ProductsFilter

    @action(methods=('get',), filter_backends=(DjangoFilterBackend, SearchFilter, OrderingFilter), filterset_class=ProductsFilter, detail=False, url_path='dashboard')
    def dashboard(self, request, *args, **kwargs):
        products = Products.objects.filter(owner=request.user)
        products = self.filter_queryset(products)
        serializer = self.get_serializer(instance=products, many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in ('list', 'dashboard'):
            return ProductsListSerializer
        elif self.action == 'create':

            cat = self.kwargs.get('cat')

            if cat == 'laptop':
                return LaptopCreateSerializer
            elif cat == 'phone':
                return PhoneCreateSerializer
            elif cat == 'tablet':
                return TabletCreateSerializer
        elif self.action == 'update' or 'partial_update':

            item = self.get_object()

            if str(item.category) == 'Laptop':
                return LaptopUpdateSerializer
            elif str(item.category) == 'Phone':
                return PhoneUpdateSerializer
            elif str(item.category) == 'Tablet':
                return TabletUpdateSerializer
        elif self.action == 'retrieve':
            item = self.get_object()

            if str(item.category) == 'Laptop':
                return LaptopDetailSerializer
            elif str(item.category) == 'Phone':
                return PhoneDetailSerializer
            elif str(item.category) == 'Tablet':
                return TabletDetailSerializer

    def get_permissions(self):
        if self.action in ('update', 'delete'):
            return [IsOwnerOrAdmin()]
        elif self.action == 'create':
            return [IsSeller()]
        else:
            return [IsAuthenticated()]


class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()

    def create(self, request, *args, **kwargs):
        item_slug = kwargs.get('item_slug')
        item = Products.objects.get(slug=item_slug)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user, product=item)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create':
            return RatingCreateSerializer
        else:
            return RatingSerializer

    def get_permissions(self):
        if self.action in ('delete', ):
            return [IsOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]


class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachments.objects.all()

    def create(self, request, *args, **kwargs):
        product = Products.objects.get(slug=kwargs.get('item_slug'))

        if product.owner != request.user:
            return Response({'MESSAGE': 'YOU ARE A BAD PROGRAMMER'})

        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(product=product)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create':
            return AttachmentsCreateSerializer
        else:
            return AttachmentsSerializer

    def get_permissions(self):
        if self.action == 'delete':
            return [IsAttachOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]
