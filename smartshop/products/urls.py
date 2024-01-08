from django.urls import path, include
from rest_framework import routers

from .routers import *
from .views import *

router = ProductsRouter()
router.register(r'products', ProductsViewSet, basename='products')

router1 = RatingsRouter()
router1.register(r'rating', RatingViewSet, basename='rating')

router2 = AttachmentsRouter()
router2.register(r'attachments', AttachmentsViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router1.urls)),
    path('', include(router2.urls)),

]
