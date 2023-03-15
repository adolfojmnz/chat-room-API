from django.db import models

from accounts.models import CustomUser as User
from msg.models import Message, Files


class Chatroom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000, blank=True, default=True)
    creation_date = models.DateField(auto_now=True)
    public = models.BooleanField(default=True)
    min_age_required = models.IntegerField(default=13)
    topics = models.ManyToManyField('chatrooms.Topic')
    participants = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)
    files = models.ManyToManyField(Files)

    def __str__(self) -> str:
        return self.name


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)
    files = models.ManyToManyField(Files)

    def __str__(self) -> str:
        return self.messages.all()[-1][:100]


class Topic(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name