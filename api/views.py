from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status

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


class ChatroomParticipantListView(ChatroomParticipantsHelperMixin, APIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwrags):
        return self.list_participants(request)

    def post(self, request, *args, **kwrags):
        return self.perform_add_or_delete_participant(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_participant(request)


class ChatroomTopicListView(ChatroomTopicHelperMixin, APIView):

    def get(self, request, *args, **kwargs):
        chatroom = self.get_chatroom_from_request(request)
        serializer = TopicSerializer(chatroom.topics.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        chatroom = self.get_chatroom_from_request(request)
        chatroom.topics.add(self.get_topic_from_request(request))
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        chatroom = self.get_chatroom_from_request(request)
        chatroom.topics.remove(self.get_topic_from_request(request))
        return self.get(request, *args, **kwargs)


class MessageListView(ListCreateAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        chatroom_id = request.parser_context['kwargs'].get('pk')
        if chatroom_id is not None:
            self.queryset = self.queryset.filter(chatroom_id=chatroom_id)
        return super().list(request, *args, **kwargs)


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
