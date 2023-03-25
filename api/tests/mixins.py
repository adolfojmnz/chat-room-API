from django.urls import reverse
from django.test import Client

from rest_framework import status

from api import serializers
from accounts.models import CustomUser as User


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

    def create_user(self):
        return self.client.post(reverse('api:users'), self.user_data)

    def update_user_date(self) -> None:
        self.user_data['username'] = 'new_username'
        self.user_data['first_name'] = 'new_first_name'
        self.user_data['last_name'] = 'new_last_name'
        self.user_data['email'] = 'new_email@localhost.com'
        self.user_data['bio'] = 'new_bio'
        self.user_data['birtdate'] = '1999-09-29'
        self.user_data['password'] = 'new_password'

    def get_access_token(self):
        data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(reverse('token_obtain_pair'), data=data)
        if response.status_code == status.HTTP_200_OK:
            return response.data.get('access')
        return None

    def build_client_with_authorization_headers(self):
        self.token = self.get_access_token()
        self.client = Client(HTTP_AUTHORIZATION=f'JWT {self.token}')

    def get_single_user_serializer(self):
        return serializers.UserSerializer(User.objects.get(username=self.user_data.get('username')))

    def get_list_user_serializer(self):
        return serializers.UserSerializer(User.objects.all(), many=True)
