from django.urls import path, include

from .routers import OrdersRouter
from .views import *


router = OrdersRouter()
router.register('orders', OrdersViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls))
]