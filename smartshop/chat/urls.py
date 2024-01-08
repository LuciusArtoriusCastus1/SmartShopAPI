from django.urls import path, include

from .routers import ChatRoomRouter
from .views import *

router = ChatRoomRouter()
router.register(r'chat', ChatRoomViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),

]
