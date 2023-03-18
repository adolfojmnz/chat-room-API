from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic, ChatroomMessage

from api.serializers import (
    UserSerializer,
    ChatroomSerializer,
    TopicSerializer,
    ChatroomMessageSerializer,
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


class TopicListView(ListCreateAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class TopicDetailView(RetrieveUpdateDestroyAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class MessageListView(ListCreateAPIView):
    model = ChatroomMessage
    queryset = model.objects.all()
    serializer_class = ChatroomMessageSerializer


class MessageDetailView(RetrieveUpdateDestroyAPIView):
    model = ChatroomMessage
    queryset = model.objects.all()
    serializer_class = ChatroomMessageSerializer
