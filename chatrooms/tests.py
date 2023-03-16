from django.test import TestCase

from chatrooms.models import Chatroom, Chat, Topic, ChatroomMessage, ChatMessage
from accounts.tests import CreateTestUserMixin


class TestChatroomMixin:

    def create_chatroom(self):
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

    def create_chatroom_message(self):
        chatroom_message = ChatroomMessage.objects.create(
            chatroom = self.chatroom,
            sender = self.user,
            body = 'Hello, world!',
        )
        return chatroom_message

    def create_chat_message(self):
        chat_message = ChatMessage.objects.create(
            chat = self.chat,
            sender = self.user,
            body = 'Hello, world!',
        )
        return chat_message


class ChatroomTest(CreateTestUserMixin, TestChatroomMixin, TestCase):

    def setUp(self) -> None:
        self.user = self.create_test_user()
        self.topic = self.create_topic()
        self.chat = self.create_chat()
        self.chatroom = self.create_chatroom()
        self.chatroom_message = self.create_chatroom_message()
        self.chat_message = self.create_chat_message()

        self.chatroom.participants.add(self.user)
        self.chatroom.topics.add(self.topic)
        self.chat.participants.add(self.user)

    def test_chatroom(self):
        chatroom = Chatroom.objects.get(name='Test Chat Room')
        self.assertEqual(chatroom.participants.get(username=self.user.username), self.user)
        self.assertEqual(chatroom.name, 'Test Chat Room')
        self.assertEqual(chatroom.description, 'A chat room intended to be used in a test suit')
        self.assertEqual(chatroom.topics.get(pk=1), self.topic)

    def test_chat(self):
        chat = Chat.objects.get(pk=1)
        self.assertEqual(chat.participants.get(username=self.user.username), self.user)

    def test_topic(self):
        topic = Topic.objects.get(pk=1)
        self.assertEqual(topic.name, self.topic.name)
        self.assertEqual(topic.description, self.topic.description)

    def test_chatroom_message(self):
        chatroom_message = ChatroomMessage.objects.get(pk=1)
        self.assertEqual(chatroom_message.chatroom, self.chatroom)
        self.assertEqual(chatroom_message.sender, self.user)
        self.assertEqual(chatroom_message.body, 'Hello, world!')

    def test_chat_message(self):
        chat_message = ChatMessage.objects.get(pk=1)
        self.assertEqual(chat_message.chat, self.chat)
        self.assertEqual(chat_message.sender, self.user)
        self.assertEqual(chat_message.body, 'Hello, world!')
