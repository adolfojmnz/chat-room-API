from django.contrib import admin

from chatrooms.models import Chatroom, Chat, Topic, ChatroomMessage, ChatMessage

admin.site.register(Chatroom)
admin.site.register(Chat)
admin.site.register(Topic)
admin.site.register(ChatroomMessage)
admin.site.register(ChatMessage)