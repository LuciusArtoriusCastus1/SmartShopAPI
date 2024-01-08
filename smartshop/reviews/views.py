from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Products
from .permissions import IsOwnerOrAdmin
from .serializers import *


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('likes', 'post_date')

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        item_slug = kwargs.get('item_slug')
        item = Products.objects.get(slug=item_slug)
        refers_to = kwargs.get('refers_to')

        if refers_to is not None:
            referred_review = Reviews.objects.get(id=refers_to)
            if referred_review.product != item:
                return Response({'MESSAGE': 'YOU ARE A BAD PROGRAMMER'})

        review = serializer_class(data=request.data, context={'request': request})
        if review.is_valid():
            if refers_to != 'none':
                review.save(product=item, refers_to=refers_to)
            else:
                review.save(product=item, refers_to=None)
            return Response(review.data, status=status.HTTP_200_OK)
        return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put', 'get'], detail=True, url_path='like/(?P<pk>[^/.]+)')
    def review_like(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                like = Like.objects.get(review__id=instance.id, owner=request.user)
            except Like.DoesNotExist:
                like = None
            likes = instance.likes
            if like is None:
                serializer.save(likes=likes + 1)
                Like.objects.create(review_id=instance.id, liked=True, owner=request.user)
            else:
                if like.liked:
                    like.liked = False
                    like.save()
                    serializer.save(likes=likes - 1)
                else:
                    like.liked = True
                    like.save()
                    serializer.save(likes=likes + 1)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False, url_path='product_review_list/(?P<item_slug>[^/.]+)')
    def product_review_list(self, request, *args, **kwargs):
        item = Products.objects.get(slug=kwargs.get('item_slug'))
        reviews = Reviews.objects.filter(product=item)
        reviews = self.filter_queryset(reviews)
        serializer = self.get_serializer(instance=reviews, many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewsCreateSerializer
        elif self.action in ('retrieve', 'list'):
            return ReviewsListSerializer
        elif self.action in ('update', 'partial_update'):
            return ReviewsUpdateSerializer
        elif self.action == 'review_like':
            return LikeReviewSerializer
        else:
            return ReviewsListSerializer

    def get_permissions(self):
        if self.action in ('update', 'delete'):
            return [IsOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]
