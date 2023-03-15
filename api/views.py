from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Chat, Topic, ChatroomMessage, ChatMessage

from api.serializers import (
    UserSerializer,
    ChatroomSerializer,
    ChatSerializer,
    TopicSerializer,
    ChatroomMessageSerializer,
    ChatMessageSerializer,
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


class ChatroomMessageListView(ListCreateAPIView):
    model = ChatroomMessage
    queryset = model.objects.all()
    serializer_class = ChatroomMessageSerializer


class ChatMessageListView(ListCreateAPIView):
    model = ChatMessage
    queryset = model.objects.all()
    serializer_class = ChatMessageSerializer
