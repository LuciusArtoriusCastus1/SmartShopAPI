import json

from channels.db import database_sync_to_async
from djangochannelsrestframework import mixins
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessagesSerializer
from customuser.models import User
from customuser.serializers import CustomUserSerializer


class ChatRoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def create_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.notify_users()

    @action()
    async def create_message(self, message, **kwargs):
        room: ChatRoom = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            chat_room=room,
            creator=self.scope["user"],
            text=message
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.chat_room.id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessagesSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: ChatRoom = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'users': await self.members(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'users': event["users"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> ChatRoom:
        return ChatRoom.objects.get(pk=pk)

    @database_sync_to_async
    def members(self, room: ChatRoom):
        return [CustomUserSerializer(user).data for user in room.members.all()]


class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


