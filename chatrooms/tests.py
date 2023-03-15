from django.test import TestCase

from chatrooms.models import Chatroom, Chat, Topic
from accounts.tests import CreateTestUserMixin
from msg.tests import CreateTestMessageMixin


class TestChatroomMixin:

    def create_test_chatroom(self):
        chatroom = Chatroom.objects.create(
            name = 'Test Chat Room',
            description = 'A chat room intended to be used in a test suit',
        )
        return chatroom

    def create_chat(self):
        chat = Chat.objects.create()
        return chat

    def create_topic(self):
        topic = Topic.objects.create(
            name = 'Test Topic',
            description = 'Topic created for testing purposes'
        )
        return topic


class ChatroomTest(CreateTestUserMixin, CreateTestMessageMixin, TestChatroomMixin, TestCase):

    def setUp(self) -> None:
        self.user = self.create_test_user()
        self.topic = self.create_topic()
        self.message = self.create_test_message()
        self.chat = self.create_chat()
        self.chatroom = self.create_test_chatroom()

        self.chatroom.participants.add(self.user)
        self.chatroom.messages.add(self.message)
        self.chatroom.topics.add(self.topic)

        self.chat.participants.add(self.user)
        self.chat.messages.add(self.message)

    def test_chatroom(self):
        chatroom = Chatroom.objects.get(name='Test Chat Room')
        self.assertEqual(chatroom.participants.get(username=self.user.username), self.user)
        self.assertEqual(chatroom.messages.get(sender__username=self.user.username), self.message)
        self.assertEqual(chatroom.name, 'Test Chat Room')
        self.assertEqual(chatroom.description, 'A chat room intended to be used in a test suit')
        self.assertEqual(chatroom.topics.get(pk=1), self.topic)

    def test_chat(self):
        chat = Chat.objects.get(pk=1)
        self.assertEqual(chat.participants.get(username=self.user.username), self.user)
        self.assertEqual(chat.messages.get(sender__username=self.user.username), self.message)

    def test_topic(self):
        topic = Topic.objects.get(pk=1)
        self.assertEqual(topic.name, self.topic.name)
        self.assertEqual(topic.description, self.topic.description)
