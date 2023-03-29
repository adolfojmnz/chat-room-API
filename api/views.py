from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Message

from api.serializers import (
    UserSerializer,
    MessageSerializer,
    ChatroomSerializer,
)
from api.mixins.views import (
    UserListViewMixin,
    UserDetailViewMixin,
    UserFriendListMixin,
    MessageListViewMixin,
    MessageDetailViewMixin,
    ChatroomListViewMixin,
    ChatroomDetailViewMixin,
    ChatroomMessageListViewMixin,
    ChatroomParticipantListViewMixin,
    ChatroomAdminListViewMixin,
)


class UserListView(UserListViewMixin, ListCreateAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class UserDetailView(UserDetailViewMixin, RetrieveUpdateDestroyAPIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer


class UserFriendListView(UserFriendListMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_friends(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_add_or_delete_friend(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_friend(request, *args, **kwargs)


class MessageListView(MessageListViewMixin, ListCreateAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(MessageDetailViewMixin, RetrieveUpdateDestroyAPIView):
    model = Message
    queryset = model.objects.all()
    serializer_class = MessageSerializer


class ChatroomListView(ChatroomListViewMixin, ListAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ChatroomDetailView(ChatroomDetailViewMixin, RetrieveUpdateDestroyAPIView):
    model = Chatroom
    queryset = model.objects.all()
    serializer_class = ChatroomSerializer


class ChatroomMessageListView(ChatroomMessageListViewMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.list_messages(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.send_message(request, *args, **kwargs)


class ChatroomAdminListView(ChatroomAdminListViewMixin, APIView):

    def get(self, request, *args, **kwrags):
        return self.list_admins(request)

    def post(self, request, *args, **kwrags):
        return self.perform_add_or_delete_admin(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_admin(request)


class ChatroomParticipantListView(ChatroomParticipantListViewMixin, APIView):

    def get(self, request, *args, **kwrags):
        return self.list_participants(request)

    def post(self, request, *args, **kwrags):
        return self.perform_add_or_delete_participant(request)

    def delete(self, request, *args, **kwargs):
        return self.perform_add_or_delete_participant(request)
