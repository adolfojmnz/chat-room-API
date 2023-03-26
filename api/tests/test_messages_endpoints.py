from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from chatrooms.models import Message
from api.tests.mixins import (
    APIRequestFactoryMixin,
    MessageMixin,
    ChatroomMixin,
    UserMixin,
)


class SetUpMixin(MessageMixin, ChatroomMixin, UserMixin, APIRequestFactoryMixin):

    def setUp(self) -> None:
        self.request = self.get_api_request()
        self.user = self.create_admin_user()
        self.client = self.get_client_with_authorization_headers()
        self.last_setup()
        return super().setUp()


class TestMessageListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def build_url(self):
        self.url = reverse('api:messages')

    def last_setup(self):
        self.build_url()
        pass

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_message_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        self.chatroom = self.create_chatroom()
        self.message = self.create_message()
        response = self.message
        serializer = self.get_single_message_serializer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestMessageDetailEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        super()
        return super().setUp()

    def build_url(self):
        self.url = reverse(
            'api:message-detail',
            kwargs = {'pk': self.message.data.get('id')},
        )

    def last_setup(self):
        self.chatroom = self.create_chatroom()
        self.message = self.create_message()
        self.build_url()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_message_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.message_data['body'] = 'new message body'
        response = self.client.patch(self.url, self.message_data, content_type='application/json')
        serializer = self.get_single_message_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        self.update_message_data()
        response = self.client.put(self.url, self.message_data, content_type='application/json')
        serializer = self.get_single_message_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(pk=self.message_data.get('id')))

