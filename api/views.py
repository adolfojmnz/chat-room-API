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


class ChatroomParticipantListView(APIView):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer

    def get_chatroom(self, request):
        pk = request.parser_context['kwargs'].get('pk')
        if pk is not None:
            try:
                return Chatroom.objects.get(pk=pk)
            except Chatroom.DoesNotExist:
                return None
        return None

    def get_participant(self, request):
        participant_id = request.POST.get('id')
        if participant_id is not None:
            try:
                return User.objects.get(pk=participant_id)
            except User.DoesNotExist:
                return None
        return None

    def get(self, request, *args, **kwrags):
        chatroom = self.get_chatroom(request)
        if isinstance(chatroom, Chatroom):
            serializer = UserSerializer(chatroom.participants.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Object not found!'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwrags):
        chatroom = self.get_chatroom(request)
        participant = self.get_participant(request)
        if not isinstance(chatroom, Chatroom):
            return Response({'Bad Request': 'Chatroom not found!'}, status=status.HTTP_404_NOT_FOUND)
        if not isinstance(participant, User):
            return Response({'Bad Request': 'Participant not found!'}, status=status.HTTP_404_NOT_FOUND)
        chatroom.participants.add(participant)
        chatroom.save()
        serializer = UserSerializer(chatroom.participants.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        chatroom = self.get_chatroom(request)
        participant = self.get_participant(request)
        if not isinstance(chatroom, Chatroom):
            return Response({'Bad Request': 'Chatroom not found!'}, status=status.HTTP_404_NOT_FOUND)
        if not isinstance(participant, User):
            return Response({'Bad Request': 'Participant not found!'}, status=status.HTTP_404_NOT_FOUND)
        chatroom.participants.remove(participant)
        chatroom.save()
        serializer = UserSerializer(chatroom.participants.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
