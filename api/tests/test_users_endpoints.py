from django.test import TestCase
from django.test import Client
from django.urls import reverse

from rest_framework import status

from api import serializers
from accounts.models import CustomUser as User


class SetUpMixin:

    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def define_user_data(self) -> None:
        self.user_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test_email@localhost.com',
            'bio': 'test_bio',
            'birtdate': '1989-09-29',
            'password': 'test_password',
        }

    def update_user_date(self) -> None:
        self.user_data['username'] = 'new_username'
        self.user_data['first_name'] = 'new_first_name'
        self.user_data['last_name'] = 'new_last_name'
        self.user_data['email'] = 'new_email@localhost.com'
        self.user_data['bio'] = 'new_bio'
        self.user_data['birtdate'] = '1999-09-29'
        self.user_data['password'] = 'new_password'

    def create_user(self):
        return self.client.post(reverse('api:users'), self.user_data)

    def get_single_user_serializer(self):
        return serializers.UserSerializer(User.objects.get(username=self.user_data.get('username')))

    def get_list_user_serializer(self):
        return serializers.UserSerializer(User.objects.all(), many=True)


class TestUserListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.url = reverse('api:users')
        self.define_user_data()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        response = self.create_user()
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestUserDetailEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.url = reverse('api:user-detail', kwargs={'pk': 1})
        self.define_user_data()
        self.user = self.create_user()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.user_data['username'] = 'new_username'
        response = self.client.patch(self.url, self.user_data, content_type='application/json')
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        self.update_user_date()
        response = self.client.put(self.url, self.user_data, content_type='application/json')
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user_data.get('username')))
