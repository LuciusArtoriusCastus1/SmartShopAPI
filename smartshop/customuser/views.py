from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customuser.models import User
from customuser.serializers import SellerSerializer


class UpgradeSellerStatus(APIView):

    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = SellerSerializer(instance=user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(seller_status=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

