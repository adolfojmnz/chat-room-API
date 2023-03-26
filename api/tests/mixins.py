from django.urls import reverse
from django.test import Client

from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api import serializers
from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Message


class APIRequestFactoryMixin:

    def get_api_request(self):
        self.factory = APIRequestFactory()
        return Request(self.factory.get('/'))


class UserMixin:
    user_data = {
        'username': 'test_username',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'email': 'test_email@localhost.com',
        'bio': 'test_bio',
        'birtdate': '1989-09-29',
        'password': 'test_password',
    }

    def create_user(self, user_data=None):
        user_data = user_data if user_data is not None else self.user_data
        return self.client.post(reverse('api:users'), user_data)

    def create_superuser(self):
        user_data = self.user_data.copy()
        user_data['username'] = 'superuser_username'
        response = self.create_user(user_data)
        user = User.objects.get(pk=response.data.get('id'))
        user.is_staff = True
        user.save()
        return response

    def update_user_data(self):
        self.user_data['username'] = 'new_username'
        self.user_data['first_name'] = 'new_first_name'
        self.user_data['last_name'] = 'new_last_name'
        self.user_data['email'] = 'new_email@localhost.com'
        self.user_data['bio'] = 'new_bio'
        self.user_data['birtdate'] = '1999-09-29'
        self.user_data['password'] = 'new_password'

    def get_access_token(self, superuser=False):
        username = self.user_data['username'] if superuser is False else 'superuser_username'
        data = {'username': username, 'password': self.user_data['password']}
        response = self.client.post(reverse('token_obtain_pair'), data=data)
        if response.status_code == status.HTTP_200_OK:
            return response.data.get('access')
        return None

    def get_client_with_authorization_headers(self, superuser=False):
        self.token = self.get_access_token(superuser)
        return Client(HTTP_AUTHORIZATION=f'JWT {self.token}')

    def get_single_user_serializer(self):
        return serializers.UserSerializer(User.objects.get(username=self.user_data.get('username')))

    def get_list_user_serializer(self):
        return serializers.UserSerializer(User.objects.all(), many=True)


class MessageMixin:

    def create_message(self):
        self.message_data = {
            'chatroom_id': self.chatroom.data.get('id'),
            'sender_id': self.user.data.get('id'),
            'body': 'message body',
        }
        return self.client.post(
            reverse('api:messages'),
            data = self.message_data,
        )

    def update_message_data(self):
        self.message_data['body'] = 'new message body'

    def get_single_message_serializer(self):
        message_id = self.message.data.get('id')
        return serializers.MessageSerializer(
            Message.objects.get(pk=message_id),
            context = {'request': self.request},
        )

    def get_list_message_serializer(self):
        return serializers.MessageSerializer(
            Message.objects.all(),
            many = True,
            context = {'request': self.request},
        )


class ChatroomMixin:
    chatroom_data = {
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

    def get_single_chatroom_serializer(self):
        return serializers.ChatroomSerializer(
            Chatroom.objects.get(
                name=self.chatroom_data.get('name'),
            ),
            context = {'request': self.request}
        )

    def get_list_chatroom_serializer(self):
        return serializers.ChatroomSerializer(
            Chatroom.objects.all(),
            many = True,
            context = {'request': self.request}
        )


class ChatroomMessageMixin:

    def create_chatroom_message(self):
        return self.client.post(
            reverse(
                'api:chatroom-messages',
                kwargs={'pk': self.chatroom.pk},
            ),
            data = {'body': 'Message body'}
        )

    def get_chatroom_message_list_serializer(self):
        return serializers.MessageSerializer(
            Message.objects.all(),
            many = True,
            context = {'request': self.request}
        )
