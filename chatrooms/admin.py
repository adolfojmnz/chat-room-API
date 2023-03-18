from django.contrib import admin

from chatrooms.models import Chatroom, Topic, Message

admin.site.register(Chatroom)
admin.site.register(Topic)
admin.site.register(Message)