from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from json import dumps

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom

from api import serializers
from api.tests.mixins import ChatroomMixin, UserMixin


class SetUpMixin(ChatroomMixin, UserMixin):

    def setUp(self):
        self.superuser_response = self.create_superuser()
        self.client = self.get_client_with_authorization_headers(superuser=True)
        self.chatroom_response = self.create_chatroom()
        self.last_setup()
        return super().setUp()


class TestChatroomParticipantListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def build_url(self):
        self.url = reverse(
            'api:chatroom-admins',
            kwargs={'pk': self.chatroom.pk},
        )

    def last_setup(self):
        self.user_response = self.create_user()
        self.admin = User.objects.get(pk=self.user_response.data.get('id'))
        self.chatroom = Chatroom.objects.get(pk=self.chatroom_response.data.get('id'))
        self.chatroom.participants.add(self.admin)
        self.chatroom.admins.add(self.admin)
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = serializers.UserSerializer(self.chatroom.admins.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.admins.all()), 2)

    def test_post(self):
        self.chatroom.admins.remove(self.admin)
        response = self.client.post(self.url, {'id': self.admin.pk})
        serializer = serializers.UserSerializer(self.chatroom.admins.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.admins.all()), 2)

    def test_delete(self):
        response = self.client.delete(self.url, dumps({'id': self.admin.pk}), content_type='application/json')
        serializer = serializers.UserSerializer(self.chatroom.admins, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.admins.all()), 1)

