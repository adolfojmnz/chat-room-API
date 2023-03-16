from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from api import serializers
from chatrooms.models import Chat


class ChatHelperMixin:

    def setUp(self):
        self.client = Client()
        return super().setUp()

    def create_chat(self):
        return self.client.post(reverse('api:chats'))

    def get_single_chat_serialized(self):
        return serializers.ChatSerializer(
            Chat.objects.get(pk=1)
        )

    def get_list_chat_serialized(self):
        return serializers.ChatSerializer(
            Chat.objects.all(),
            many = True
        )


class TestChatListEndpoint(ChatHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chats')
        self.create_chat()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_chat_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        response = self.create_chat()
        serializer = self.get_single_chat_serialized()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestChatDetailEndpoint(ChatHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chat-detail', kwargs={'pk': 1})
        self.create_chat()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_chat_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Chat.objects.filter(pk=1))
