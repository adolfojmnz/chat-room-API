from django.test import TestCase

from chatrooms.models import Chatroom, Message
from accounts.tests import CreateTestUserMixin


class TestChatroomMixin:

    def create_chatroom(self):
        chatroom = Chatroom.objects.create(
            name = 'Test Chat Room',
            description = 'A chat room intended to be used in a test suit',
        )
        return chatroom

    def create_chatroom_message(self):
        chatroom_message = Message.objects.create(
            chatroom = self.chatroom,
            sender = self.user,
            body = 'Hello, world!',
        )
        return chatroom_message


class ChatroomTest(CreateTestUserMixin, TestChatroomMixin, TestCase):

    def setUp(self) -> None:
        self.user = self.create_test_user()
        self.chatroom = self.create_chatroom()
        self.chatroom_message = self.create_chatroom_message()
        self.chatroom.participants.add(self.user)

    def test_chatroom(self):
        chatroom = Chatroom.objects.get(name='Test Chat Room')
        self.assertEqual(chatroom.participants.get(username=self.user.username), self.user)
        self.assertEqual(chatroom.name, 'Test Chat Room')
        self.assertEqual(chatroom.description, 'A chat room intended to be used in a test suit')

    def test_chatroom_message(self):
        chatroom_message = Message.objects.get(pk=self.chatroom_message.pk)
        self.assertEqual(chatroom_message.chatroom, self.chatroom)
        self.assertEqual(chatroom_message.sender, self.user)
        self.assertEqual(chatroom_message.body, 'Hello, world!')
