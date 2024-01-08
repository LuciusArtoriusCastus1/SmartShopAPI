from django.contrib import admin

from .models import *


class ChatRoomConfig(admin.ModelAdmin):
    list_display = ('id', 'product', 'created_at', 'updated_at')
    list_filter = ('product', 'members', 'created_at', )
    list_display_links = ('id', )
    readonly_fields = ('members', 'created_at', 'updated_at', )


class MessageConfig(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'creator', 'text', 'created_at', )
    list_filter = ('chat_room', 'creator', 'created_at', )
    list_display_links = ('id', )


admin.site.register(ChatRoom, ChatRoomConfig)
admin.site.register(Message, MessageConfig)
