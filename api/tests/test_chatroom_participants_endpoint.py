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
        self.user_response = self.create_user()
        self.client = self.get_client_with_authorization_headers()
        self.chatroom_response = self.create_chatroom()
        self.last_setup()
        return super().setUp()


class TestChatroomParticipantListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def build_url(self):
        self.url = reverse(
            'api:chatroom-participants',
            kwargs={'pk': self.chatroom.pk},
        )

    def last_setup(self):
        self.participant = User.objects.get(pk=self.user_response.data.get('id'))
        self.chatroom = Chatroom.objects.get(pk=self.chatroom_response.data.get('id'))
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = serializers.UserSerializer(self.chatroom.participants.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 1)

    def test_post(self):
        self.chatroom.participants.remove(self.participant)
        response = self.client.post(self.url, {'id': self.participant.pk})
        serializer = serializers.UserSerializer(self.chatroom.participants.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 1)

    def test_delete(self):
        response = self.client.delete(self.url, dumps({'id': self.participant.pk}), content_type='application/json')
        serializer = serializers.UserSerializer(self.chatroom.participants, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(self.chatroom.participants.all()), 0)
