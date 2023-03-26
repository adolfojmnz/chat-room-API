from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from chatrooms.models import Chatroom
from api.tests.mixins import (
    APIRequestFactoryMixin,
    ChatroomMixin,
    UserMixin,
)


class SetUpMixin(ChatroomMixin, UserMixin, APIRequestFactoryMixin):

    def setUp(self):
        self.request = self.get_api_request()
        self.user = self.create_user()
        self.client = self.get_client_with_authorization_headers()
        self.last_setup()
        return super().setUp()


class TestChatroomListEndpoint(SetUpMixin, TestCase):

    def setUp(self):
        return super().setUp()

    def build_url(self):
        self.url = reverse('api:chatrooms')

    def last_setup(self):
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_chatroom_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        response = self.create_chatroom()
        serializer = self.get_single_chatroom_serializer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestChatroomDetailEndpoint(SetUpMixin, TestCase):

    def setUp(self):
        return super().setUp()

    def build_url(self):
        self.url = reverse(
            'api:chatroom-detail', kwargs={'pk': self.chatroom.data.get('id')}
        )

    def last_setup(self):
        self.chatroom = self.create_chatroom()
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_chatroom_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.chatroom_data['name'] = 'new name'
        response = self.client.patch(self.url, self.chatroom_data, content_type='application/json')
        serializer = self.get_single_chatroom_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        self.update_chatroom_data()
        response = self.client.put(self.url, self.chatroom_data, content_type='application/json')
        serializer = self.get_single_chatroom_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Chatroom.objects.filter(name=self.chatroom_data.get('name')))
