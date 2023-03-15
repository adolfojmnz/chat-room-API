from django.contrib import admin

from chatrooms.models import Chatroom, Chat, Topic

admin.site.register(Chatroom)
admin.site.register(Chat)
admin.site.register(Topic)