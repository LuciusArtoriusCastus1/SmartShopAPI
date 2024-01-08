from django.urls import path, include

from .routers import *
from .views import *

router = ReviewsRouter()
router.register(r'reviews', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
