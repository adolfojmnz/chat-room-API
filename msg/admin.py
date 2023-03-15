from django.contrib import admin

from msg.models import Message, Files


admin.site.register(Message)
admin.site.register(Files)