from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Chat, Topic
from msg.models import Message, Files

from api.serializers import (
    UserSerializer,
    ChatroomSerializer,
    ChatSerializer,
    TopicSerializer,
    MessageSerializer,
    FileSerializer,
)


class UserListView(ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class ChatroomListView(ListCreateAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatListView(ListCreateAPIView):
    model = Chat
    queryset = model.objects.all()
    serializer_class = ChatSerializer


class TopicListView(ListCreateAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class MessageListView(ListCreateAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class FileListView(ListCreateAPIView):
    model = Files
    queryset = model.objects.all()
    serializer_class = FileSerializer
