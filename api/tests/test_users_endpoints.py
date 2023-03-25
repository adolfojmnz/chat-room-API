from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from accounts.models import CustomUser as User
from api.tests.mixins import UserMixin


class SetUpMixin(UserMixin):

    def setUp(self) -> None:
        self.client = self.get_client_with_authorization_headers()
        return super().setUp()


class TestUserListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.url = reverse('api:users')
        self.user = self.create_user()
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_list_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        self.user_data['username'] = 'new_test_username'
        response = self.create_user()
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestUserDetailEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.user = self.create_user()
        pk = self.user.data.get('id')
        self.url = reverse('api:user-detail', kwargs={'pk': pk})
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
        self.update_user_data()
        response = self.client.put(self.url, self.user_data, content_type='application/json')
        serializer = self.get_single_user_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user_data.get('username')))
