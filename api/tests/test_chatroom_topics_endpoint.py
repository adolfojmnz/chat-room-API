from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

import json

from api import serializers
from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic


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


class TopicHelperMixin(UserHelperMixin, ChatroomHelperMixin):
    topic_data = {
        'name': 'test topic',
        'description': 'test description',
    }

    def setUp(self):
        self.client = Client()
        self.url = reverse('api:chatroom-topics', kwargs={'pk': 1})
        self.create_user()
        self.create_topic()
        self.create_chatroom()
        return super().setUp()

    def create_topic(self):
        return Topic.objects.create(
            name = self.topic_data['name'],
            description = self.topic_data['description'],
        )


class TestChatroomTopicListEndpoint(TopicHelperMixin, TestCase):

    def setUp(self):
        return super().setUp()

    def test_get(self):
        chatroom = Chatroom.objects.get(pk=1)
        chatroom.topics.add(Topic.objects.get(pk=1))
        response = self.client.get(self.url)
        serializer = serializers.TopicSerializer(chatroom.topics.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(response.data, [])

    def test_post(self):
        response = self.client.post(self.url, json.dumps({'id': 1}), content_type='application/json')
        serializer = serializers.TopicSerializer(Chatroom.objects.get(pk=1).topics.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(response.data, [])

    def test_delete(self):
        response = self.client.delete(self.url, json.dumps({'id': 1}), content_type='application/json')
        serializer = serializers.TopicSerializer(Chatroom.objects.get(pk=1).topics.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data, [])
