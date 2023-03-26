from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from json import dumps

from chatrooms.models import Chatroom, Topic
from api.tests.mixins import (
    UserMixin,
    TopicMixin,
    ChatroomMixin,
    ChatroomTopicMixin,
)


class SetUpMixin(UserMixin, TopicMixin, ChatroomMixin, ChatroomTopicMixin):

    def setUp(self):
        self.create_user()
        self.client = self.get_client_with_authorization_headers()
        self.chatroom_response = self.create_chatroom()
        self.topic_response = self.create_topic()
        self.last_setup()
        return super().setUp()


class TestChatroomTopicListEndpoint(SetUpMixin, TestCase):

    def setUp(self):
        return super().setUp()

    def build_url(self):
        self.url = reverse(
            'api:chatroom-topics',
            kwargs = {'pk': self.topic_response.data.get('id')},
        )

    def last_setup(self):
        self.topic = Topic.objects.get(pk=self.topic_response.data.get('id'))
        self.chatroom = Chatroom.objects.get(pk=self.chatroom_response.data.get('id'))
        self.chatroom.topics.add(self.topic)
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_chatroom_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.chatroom.topics.all().count(), 1)

    def test_post(self):
        self.chatroom.topics.remove(self.topic)
        response = self.client.post(self.url, dumps({'id': self.topic.pk}), content_type='application/json')
        serializer = self.get_list_chatroom_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.chatroom.topics.all().count(), 1)

    def test_delete(self):
        response = self.client.delete(self.url, dumps({'id': self.topic.pk}), content_type='application/json')
        serializer = self.get_list_chatroom_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(self.chatroom.topics.all().count(), 0)
