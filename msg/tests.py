from django.test import TestCase

from msg.models import Message
from accounts.tests import CreateTestUserMixin


class CreateTestMessageMixin:

    def create_test_message(self):
        message = Message.objects.create(
            sender = self.user,
            body = 'test body message',
        )
        return message


class MessageTest(CreateTestUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_test_user()
        self.message = self.create_test_message()
        self.user.save()
        self.message.save()

    def test_message(self):
        self.assertTrue(Message.objects.filter(sender__username=self.user.username).exists())
        self.assertEqual(Message.objects.get(sender__username=self.user.username).body, self.message.body)