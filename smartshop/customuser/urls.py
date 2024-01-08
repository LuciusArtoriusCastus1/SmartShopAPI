from django.urls import path

from customuser.views import UpgradeSellerStatus

urlpatterns = [
    path('customuser/sellerstatus/', UpgradeSellerStatus.as_view())
]
