from django.test import TestCase

from accounts.models import CustomUser as User
from msg.models import Message


class MessageTest(TestCase):

    def setUp(self):
        user = User.objects.create(
            username = 'test-user',
            email = 'user@testsuit.com',
            password = 'test$psswd',
        )
        user.save()
        self.user = user
        message = Message.objects.create(
            sender = user,
            body = 'test body message',
        )
        message.save()
        self.message = message

    def test_message(self):
        self.assertTrue(Message.objects.filter(sender__username=self.user.username).exists())
        self.assertEqual(Message.objects.get(sender__username=self.user.username).body, self.message.body)