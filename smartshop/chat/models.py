from django.db import models

from customuser.models import User
from products.models import Products


class ChatRoom(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='chatrooms')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, related_name='chatrooms')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-updated_at', )


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=300)

