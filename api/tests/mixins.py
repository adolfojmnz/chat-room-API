from django.urls import reverse
from rest_framework import status
from django.test import Client


class AccessTokenMixin:

    def get_access_token(self, username, password):
        data = {'username': username, 'password': password}
        response = self.client.post(reverse('token_obtain_pair'), data=data)
        if response.status_code == status.HTTP_200_OK:
            return response.data.get('access')
        return None


class BuildClientInstanceMixin:

    def build_client(self):
        self.create_user()
        self.token = self.get_access_token(
            username = self.user_data['username'],
            password = self.user_data['password'],
        )
        self.client = Client(HTTP_AUTHORIZATION=f'JWT {self.token}')
