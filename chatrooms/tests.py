from django.test import TestCase

from chatrooms.models import Chatroom, Topic, ChatroomMessage
from accounts.tests import CreateTestUserMixin


class TestChatroomMixin:

    def create_chatroom(self):
        chatroom = Chatroom.objects.create(
            name = 'Test Chat Room',
            description = 'A chat room intended to be used in a test suit',
        )
        return chatroom

    def create_chatroom_message(self):
        chatroom_message = ChatroomMessage.objects.create(
            chatroom = self.chatroom,
            sender = self.user,
            body = 'Hello, world!',
        )
        return chatroom_message

    def create_topic(self):
        topic = Topic.objects.create(
            name = 'Test Topic',
            description = 'Topic created for testing purposes'
        )
        return topic


class ChatroomTest(CreateTestUserMixin, TestChatroomMixin, TestCase):

    def setUp(self) -> None:
        self.user = self.create_test_user()
        self.chatroom = self.create_chatroom()
        self.topic = self.create_topic()
        self.chatroom_message = self.create_chatroom_message()

        self.chatroom.participants.add(self.user)
        self.chatroom.topics.add(self.topic)

    def test_chatroom(self):
        chatroom = Chatroom.objects.get(name='Test Chat Room')
        self.assertEqual(chatroom.participants.get(username=self.user.username), self.user)
        self.assertEqual(chatroom.name, 'Test Chat Room')
        self.assertEqual(chatroom.description, 'A chat room intended to be used in a test suit')
        self.assertEqual(chatroom.topics.get(pk=1), self.topic)

    def test_chatroom_message(self):
        chatroom_message = ChatroomMessage.objects.get(pk=1)
        self.assertEqual(chatroom_message.chatroom, self.chatroom)
        self.assertEqual(chatroom_message.sender, self.user)
        self.assertEqual(chatroom_message.body, 'Hello, world!')

    def test_topic(self):
        topic = Topic.objects.get(pk=1)
        self.assertEqual(topic.name, self.topic.name)
        self.assertEqual(topic.description, self.topic.description)
