from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from api.tests.mixins import TopicMixin, UserMixin
from chatrooms.models import Topic


class SetUpMixin(TopicMixin, UserMixin):

    def setUp(self) -> None:
        self.create_user()
        self.client = self.get_client_with_authorization_headers()
        return super().setUp()


class TestTopicListEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.url = reverse('api:topics')
        return super().setUp()

    def test_get(self):
        self.create_topic()
        response = self.client.get(self.url)
        serializer = self.get_list_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post(self):
        self.topic_data['name'] = 'new_topic_name'
        response = self.create_topic()
        serializer = self.get_single_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class TestTopicDetailEndpoint(SetUpMixin, TestCase):

    def setUp(self) -> None:
        self.topic_response = self.create_topic()
        self.url = reverse(
            'api:topic-detail',
            kwargs = {'pk': self.topic_response.data.get('id')},
        )
        return super().setUp()

    def test_get(self):
        response = self.client.get(self.url)
        serializer = self.get_single_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_patch(self):
        self.topic_data['name'] = 'new_topic_name'
        response = self.client.patch(self.url, self.topic_data, content_type='application/json')
        serializer = self.get_single_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put(self):
        self.update_topic_data()
        response = self.client.put(self.url, self.topic_data, content_type='application/json')
        serializer = self.get_single_topic_serializer()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Topic.objects.filter(name=self.topic_data.get('name')))
