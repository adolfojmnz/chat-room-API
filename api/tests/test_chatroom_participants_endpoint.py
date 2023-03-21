from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from api import serializers
from accounts.models import CustomUser as User
from chatrooms.models import Chatroom

import json


class UserHelperMixin:
    user_data = {
        'username': 'test_username',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'email': 'test_email@localhost.com',
        'bio': 'test_bio',
        'birtdate': '1989-09-29',
        'password': 'test_password',
    }

    def create_user(self):
        return self.client.post(reverse('api:users'), self.user_data)


class ChatroomHelperMixin:
    chatroom_data = {
        'name': 'test name',
        'description': 'test description',
        'creation_date': '2023-03-16',
        'public': True,
        'min_age_required': 13,
    }

    def create_chatroom(self):
        return self.client.post(
            reverse('api:chatrooms'),
            self.chatroom_data,
        )


class ChatroomParticipanMixin(UserHelperMixin, ChatroomHelperMixin):

    def setUp(self):
        self.url = reverse('api:chatroom-participants', kwargs={'pk': 1})
        self.client = Client()
        self.create_user()
        self.create_chatroom()
        self.participant = User.objects.get(pk=1)
        self.chatroom = Chatroom.objects.get(pk=1)
        return super().setUp()


class TestChatroomParticipantListEndpoint(ChatroomParticipanMixin, TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_get(self):
        self.chatroom.participants.add(self.participant)
        response = self.client.get(self.url)
        serializer = serializers.UserSerializer(self.chatroom.participants.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 1)

    def test_post(self):
        response = self.client.post(self.url, {'id': 1})
        serializer = serializers.UserSerializer(self.chatroom.participants.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 1)

    def test_delete(self):
        self.chatroom.participants.add(self.participant)
        response = self.client.delete(self.url, json.dumps({'id': 1}), content_type='application/json')
        serializer = serializers.UserSerializer(self.chatroom.participants, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 0)
