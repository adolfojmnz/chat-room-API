from django.contrib import admin

from chatrooms.models import Chatroom, Message

admin.site.register(Chatroom)
admin.site.register(Message)