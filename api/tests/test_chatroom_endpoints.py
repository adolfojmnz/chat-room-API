from django.test import TestCase
from django.test import Client
from django.urls import reverse

from rest_framework import status

from api import serializers
from accounts.models import CustomUser as User
from chatrooms.models import Chatroom


class ChatroomHelperMixin:

    def setUp(self):
        self.client = Client()
        return super().setUp()

    def define_chatroom_data(self):
        self.chatroom_data = {
            'name': 'test name',
            'description': 'test description',
            'creation_date': '2023-03-16',
            'public': True,
            'min_age_required': 13,
        }

    def update_chatroom_data(self):
        self.chatroom_data['name'] = 'new test name'
        self.chatroom_data['description'] = 'new test description'
        self.chatroom_data['creation_date'] = '2023-02-16'
        self.chatroom_data['public'] = False
        self.chatroom_data['min_age_required'] = 18

    def create_chatroom(self):
        return self.client.post(
            reverse('api:chatrooms'),
            self.chatroom_data,
        )

    def get_single_chatroom_serialized(self):
        return serializers.ChatroomSerializer(
            Chatroom.objects.get(
                name=self.chatroom_data.get('name')
            )
        )

    def get_list_chatroom_serialized(self):
        return serializers.ChatroomSerializer(
            Chatroom.objects.all(),
            many = True
        )


class TestChatroomListEndpoint(ChatroomHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chatrooms')
        self.define_chatroom_data()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_chatroom_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        response = self.create_chatroom()
        serializer = self.get_single_chatroom_serialized()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestChatroomDetailEndpoint(ChatroomHelperMixin, TestCase):

    def setUp(self):
        self.url = reverse('api:chatroom-detail', kwargs={'pk': 1})
        self.define_chatroom_data()
        self.create_chatroom()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_chatroom_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.chatroom_data['name'] = 'new name'
        response = self.client.patch(self.url, self.chatroom_data, content_type='application/json')
        serializer = self.get_single_chatroom_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        self.update_chatroom_data()
        response = self.client.put(self.url, self.chatroom_data, content_type='application/json')
        serializer = self.get_single_chatroom_serialized()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Chatroom.objects.filter(name=self.chatroom_data.get('name')))
