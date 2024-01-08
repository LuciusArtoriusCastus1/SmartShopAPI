from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatRoom
from .permissions import IsMemberOrAdmin
from .serializers import ChatRoomSerializer
from products.models import Products


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def create(self, request, *args, **kwargs):
        product = Products.objects.get(slug=kwargs.get('item_slug'))
        owner = product.owner
        if owner == request.user:
            return Response({'MESSAGE': 'CURRENT USER IS THE OWNER OF THIS PRODUCT'})
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(product=product, members=[request.user, owner])

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False, url_path='user_chat_list')
    def user_caht_list(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=ChatRoom.objects.filter(members__in='request.user'), many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ('delete', 'retrieve', 'list'):
            return [IsMemberOrAdmin()]
        else:
            return [IsAuthenticated()]
