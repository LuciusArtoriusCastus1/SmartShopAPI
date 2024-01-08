from rest_framework import serializers

from chat.models import ChatRoom
from .models import Message


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)
    members = serializers.ManyRelatedField(child_relation=serializers.SlugRelatedField(slug_field='display_name', read_only=True), read_only=True)
    messages = MessagesSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'


