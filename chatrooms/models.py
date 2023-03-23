from django.db import models
from django.utils import timezone

from accounts.models import CustomUser as User


class Chatroom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True, default='')
    creation_date = models.DateField(auto_now=True)
    public = models.BooleanField(default=True)
    min_age_required = models.IntegerField(default=13)
    topics = models.ManyToManyField('chatrooms.Topic', related_name='chatrooms')
    participants = models.ManyToManyField(User, related_name='chatrooms')
    admins = models.ManyToManyField(User, related_name='admin_of_chatrooms')

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    chatroom = models.ForeignKey(Chatroom, blank=True, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='messages')
    body = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender.username}: {self.body[:100]}'


class Topic(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
