from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Message
from api.tests.mixins import (
    APIRequestFactoryMixin,
    UserMixin,
    ChatroomMessageMixin,
    ChatroomMixin,
)


class SetUpMixin(APIRequestFactoryMixin, UserMixin, ChatroomMessageMixin, ChatroomMixin):

    def setUp(self):
        self.request = self.get_api_request()
        self.url = reverse('api:chatroom-messages', kwargs={'pk': self.chatroom.pk})
        return super().setUp()


class TestChatroomMessageListEndpoint(SetUpMixin, TestCase):

    def setUp(self):
        self.user_response = self.create_user()
        self.client = self.get_client_with_authorization_headers()
        chatroom_response = self.create_chatroom()
        self.chatroom = Chatroom.objects.get(pk=chatroom_response.data.get('id'))
        self.sender = User.objects.get(pk=self.user_response.data.get('id'))
        return super().setUp()

    def test_get(self):
        Message.objects.create(
            body = 'helloo',
            chatroom = self.chatroom,
            sender = self.sender,
        )
        response = self.client.get(self.url)
        serializer = self.get_chatroom_message_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(User.objects.all().count(), 1)

    def test_post(self):
        response = self.create_chatroom_message()
        serializer = self.get_chatroom_message_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Message.objects.filter(pk=response.data[0].get('id')).exists())
