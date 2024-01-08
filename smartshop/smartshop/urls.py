from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .yasg import urlpatterns as yasg_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('orders.urls')),
    path('', include('core.urls')),
    path('', include('customuser.urls')),
    path('', include('products.urls')),
    path('', include('chat.urls')),
    path('', include('reviews.urls')),

    path('djoser/auth/', include('djoser.urls')),
    path('token/auth/', include('djoser.urls.authtoken')),
    path('jwt/auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('social/auth/', include('drf_social_oauth2.urls', namespace='drf')),
]

urlpatterns += yasg_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
