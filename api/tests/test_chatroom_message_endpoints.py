from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api import serializers
from chatrooms.models import Message


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
    chatroom_message_data = {
        'name': 'test name',
        'description': 'test description',
        'creation_date': '2023-03-16',
        'public': True,
        'min_age_required': 13,
    }

    def create_chatroom(self):
        return self.client.post(
            reverse('api:chatrooms'),
            self.chatroom_message_data,
        )


class ChatroomMessageHelperMixin(UserHelperMixin, ChatroomHelperMixin):

    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.request = Request(self.factory.get('/'))
        return super().setUp()

    def create_chatroom_message(self):
        self.chatroom_message_data = {
            'chatroom': reverse('api:chatroom-detail', kwargs={'pk': 1}),
            'sender': reverse('api:user-detail', kwargs={'pk': 1}),
            'body': 'test body',
        }
        return self.client.post(
            reverse('api:chatroom-messages'),
            self.chatroom_message_data,
        )

    def get_chatroom_message_single_serialized(self):
        return serializers.MessageSerializer(
            Message.objects.get(pk=1),
            context = {'request': self.request},
        )

    def get_chatroom_message_list_serialized(self):
        return serializers.MessageSerializer(
            Message.objects.all(),
            many = True,
            context = {'request': self.request}
        )


class TestChatroomMessageListEndpoint(ChatroomMessageHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chatroom-messages')
        self.chatroom = self.create_chatroom()
        self.sender = self.create_user()
        return super().setUp()

    def test_get(self):
        self.create_chatroom_message()
        response = self.client.get(self.url)
        serializer = self.get_chatroom_message_list_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        response = self.create_chatroom_message()
        serializer = self.get_chatroom_message_single_serialized()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Message.objects.filter(pk=1).exists())


class TestChatroomMessageDetailEndpoint(ChatroomMessageHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chatroom-message-detail', kwargs={'pk': 1})
        self.chatroom = self.create_chatroom()
        self.sender = self.create_user()
        self.chatroom_message = self.create_chatroom_message()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_chatroom_message_single_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.chatroom_message_data['body'] = 'new test body'
        response = self.client.patch(
            self.url,
            self.chatroom_message_data,
            content_type='application/json',
        )
        serializer = self.get_chatroom_message_single_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(pk=1).exists())
