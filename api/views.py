from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic, Message

from api.serializers import (
    UserSerializer,
    TopicSerializer,
    MessageSerializer,
    ChatroomSerializer,
)
from api.mixins.views import (
    UserListViewMixin,
    MessageListViewMixin,
    TopicListViewMixin,
    ChatroomListViewMixin,
    ChatroomParticipantListViewMixin,
    ChatroomTopicListViewMixin,
    ChatroomMessageListViewMixin,
)
from api.mixins.permissions import (
    UserPermissionsMixin,
)


class UserListView(UserPermissionsMixin, UserListViewMixin, ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class UserDetailView(UserPermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class TopicListView(TopicListViewMixin, ListCreateAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class TopicDetailView(RetrieveUpdateDestroyAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class MessageListView(MessageListViewMixin, ListCreateAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(RetrieveUpdateDestroyAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class ChatroomListView(ChatroomListViewMixin, ListAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ChatroomDetailView(RetrieveUpdateDestroyAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatroomTopicListView(ChatroomTopicListViewMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_topics(request)

    def post(self, request, *args, **kwargs):
        return self.perform_add_or_remove_topic(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_remove_topic(request)


class ChatroomMessageListView(ChatroomMessageListViewMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_messages(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.send_message(request, *args, **kwargs)


class ChatroomParticipantListView(ChatroomParticipantListViewMixin, APIView):

    def get(self, request, *args, **kwrags):
        return self.list_participants(request)

    def post(self, request, *args, **kwrags):
        return self.perform_add_or_delete_participant(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_participant(request)
