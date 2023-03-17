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


class UserDetailView(RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class ChatroomListView(ListCreateAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatroomDetailView(RetrieveUpdateDestroyAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatListView(ListCreateAPIView):
    model = Chat
    queryset = model.objects.all()
    serializer_class = ChatSerializer


class ChatDetailView(RetrieveUpdateDestroyAPIView):
    model = Chat
    queryset = model.objects.all()
    serializer_class = ChatSerializer


class TopicListView(ListCreateAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class TopicDetailView(RetrieveUpdateDestroyAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class AllChatroomMessagesView(ListCreateAPIView):
    model = ChatroomMessage
    queryset = model.objects.all()
    serializer_class = ChatroomMessageSerializer


class ChatroomMessageDetailView(RetrieveUpdateDestroyAPIView):
    model = ChatroomMessage
    queryset = model.objects.all()
    serializer_class = ChatroomMessageSerializer


class AllChatMessagesView(ListCreateAPIView):
    model = ChatMessage
    queryset = model.objects.all()
    serializer_class = ChatMessageSerializer


class ChatMessageDetailView(RetrieveUpdateDestroyAPIView):
    model = ChatMessage
    queryset = model.objects.all()
    serializer_class = ChatMessageSerializer
