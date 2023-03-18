from django.contrib import admin

from chatrooms.models import Chatroom, Topic, ChatroomMessage

admin.site.register(Chatroom)
admin.site.register(Topic)
admin.site.register(ChatroomMessage)