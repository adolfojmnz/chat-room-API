from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic, Message

from api.serializers import (
    UserSerializer,
    ChatroomSerializer,
    TopicSerializer,
    MessageSerializer,
)
from api.mixins.views import (
    ChatroomParticipantsHelperMixin,
    ChatroomTopicHelperMixin,
    ChatroomMessageHelperMixin,
)


class UserListView(ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class MessageListView(ListCreateAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(RetrieveUpdateDestroyAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class TopicListView(ListCreateAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class TopicDetailView(RetrieveUpdateDestroyAPIView):
    model = Topic
    queryset = model.objects.all()
    serializer_class = TopicSerializer


class ChatroomListView(ListCreateAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatroomDetailView(RetrieveUpdateDestroyAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatroomParticipantListView(ChatroomParticipantsHelperMixin, APIView):

    def get(self, request, *args, **kwrags):
        return self.list_participants(request)

    def post(self, request, *args, **kwrags):
        return self.perform_add_or_delete_participant(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_participant(request)


class ChatroomTopicListView(ChatroomTopicHelperMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_topics(request)

    def post(self, request, *args, **kwargs):
        return self.perform_add_or_remove_topic(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_remove_topic(request)


class ChatroomMessageListView(ChatroomMessageHelperMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_messages(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.send_message(request, *args, **kwargs)
