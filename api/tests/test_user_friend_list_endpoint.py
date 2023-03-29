from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from json import dumps

from accounts.models import CustomUser as User
from api.tests.mixins import UserMixin, UserFriendListMixin


class SetUpMixin(UserMixin, UserFriendListMixin):

    def setUp(self):
        self.client = self.get_client()
        self.user = self.get_user()
        self.last_setup()
        return super().setUp()

    def get_client(self):
        self.user_response = self.create_user()
        return self.get_client_with_authorization_headers()

    def get_user(self):
        return User.objects.get(pk=self.user_response.data.get('id'))

    def last_setup(self):
        self.create_user_list()
        self.user.friends.set(User.objects.all())
        self.user.clean_friends()
        self.target = self.user.friends.all()[0]
        self.url = reverse('api:user-friends', kwargs={'pk': self.user.pk})


class TestUserFriendListEndpoint(SetUpMixin, TestCase):

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_friend_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data != [])

    def test_delete(self):
        response = self.client.delete(
            self.url,
            dumps({'id': self.target.pk}),
            content_type = 'application/json',
        )
        serializer = self.get_friend_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertFalse(self.user.friends.filter(pk=self.target.pk).exists())

    def test_post(self):
        response = self.client.post(
            self.url,
            dumps({'id': self.target.pk}),
            content_type = 'application/json',
        )
        serializer = self.get_friend_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(self.user.friends.filter(pk=self.target.pk).exists())

    def test_user_cant_be_user_friend(self):
        response = self.client.post(
            self.url,
            dumps({'id': self.user.pk}),
            content_type = 'application/json',
        )
        serializer = self.get_friend_list_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertFalse(self.user.friends.filter(pk=self.user.pk).exists())
