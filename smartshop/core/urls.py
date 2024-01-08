from django.urls import path, include
from rest_framework import routers

from .routers import CartRouter
from .views import *

router = CartRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
