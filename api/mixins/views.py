from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic

from api.serializers import (
    UserSerializer,
    TopicSerializer,
    MessageSerializer,
    ChatroomMessageSerialzier,
)


class GetUserMixin:

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else self.queryset

        username = self.request.query_params.get('username')
        if username is not None:
            self.queryset = self.queryset.filter(username__icontains=username).distinct()
        first_name = self.request.query_params.get('first_name')
        if first_name is not None:
            self.queryset = self.queryset.filter(first_name__icontains=first_name).distinct()
        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            self.queryset = self.queryset.filter(last_name__icontains=last_name).distinct()
        email = self.request.query_params.get('email')
        if email is not None:
            self.queryset = self.queryset.filter(email__icontains=email)

        return self.queryset


class GetMessageMixin:

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else self.queryset

        body = self.request.query_params.get('body')
        if body is not None:
            self.queryset = self.queryset.filter(body__icontains=body).distinct()
        sender = self.request.query_params.get('sender')
        if sender is not None:
            self.queryset = self.queryset.filter(sender__username=sender)

        return self.queryset


class GetTopicMixin:

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else self.queryset

        name = self.request.query_params.get('name')
        if name is not None:
            self.queryset =  self.queryset.filter(name__icontains=name)
        description = self.request.query_params.get('description')
        if description is not None:
            self.queryset = self.queryset.filter(description__icontains=description)

        return self.queryset


class GetChatroomMixin:

    def get_chatroom_from_request(self, request):
        chatroom_id = request.parser_context['kwargs'].get('pk')
        try:
            return Chatroom.objects.get(pk=chatroom_id)
        except Chatroom.DoesNotExist:
            return None


class UserListViewHelperMixin(GetUserMixin):

    def get_queryset(self, queryset=None):
        return super().get_queryset(queryset)


class MessageListHelperMixin(GetMessageMixin):

    def get_queryset(self, queryset=None):
        return super().get_queryset(queryset)


class TopicListHelperMixin(GetTopicMixin):

    def get_queryset(self, queryset=None):
        return super().get_queryset(queryset)


class ChatroomListHelperMixin:

    def get_queryset(self):
        self.queryset = self.queryset.filter(public=True)

        name = self.request.query_params.get('name')
        topic = self.request.query_params.get('topic')
        if name is not None:
            self.queryset = self.queryset.filter(name__icontains=name).distinct()
        if topic is not None:
            self.queryset = self.queryset.filter(topics__name__icontains=topic).distinct()
        return self.queryset


class ChatroomTopicHelperMixin(GetTopicMixin, GetChatroomMixin):

    def get_topic_from_request(self, request):
        topic_id = request.data.get('id')
        try:
            return Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return None

    def list_topics(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer = TopicSerializer(
                self.get_queryset(queryset=chatroom.topics.all()),
                many = True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Object not found!'}, status=status.HTTP_404_NOT_FOUND)

    def perform_add_or_remove_topic(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if not isinstance(chatroom, Chatroom):
            return Response({'Bad Request': f'Chatroom not found!'}, status=status.HTTP_404_NOT_FOUND)
        topic = self.get_topic_from_request(request)
        if not isinstance(topic, Topic):
            return Response({'Bad Request': f'Topic not found!'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            chatroom.topics.add(topic)
        if request.method == 'DELETE':
            chatroom.topics.remove(topic)

        serializer = TopicSerializer(chatroom.topics.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatroomParticipantsHelperMixin(GetUserMixin, GetChatroomMixin):

    def get_queryset(self, queryset=None):
        return super().get_queryset(queryset)

    def get_participant_from_request(self, request):
        participant_id = request.data.get('id')
        try:
            return User.objects.get(pk=participant_id)
        except User.DoesNotExist:
            return None

    def list_participants(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer = UserSerializer(
                self.get_queryset(queryset=chatroom.participants.all()),
                many = True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Object not found!'}, status=status.HTTP_404_NOT_FOUND)

    def perform_add_or_delete_participant(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if not isinstance(chatroom, Chatroom):
            return Response({'Bad Request': f'Chatroom not found!'}, status=status.HTTP_404_NOT_FOUND)
        participant = self.get_participant_from_request(request)
        if not isinstance(participant, User):
            return Response({'Bad Request': f'Participant not found!'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            chatroom.participants.add(participant)
        if request.method == 'DELETE':
            chatroom.participants.remove(participant)

        serializer = UserSerializer(chatroom.participants.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatroomMessageHelperMixin(GetMessageMixin, GetChatroomMixin):

    def list_messages(self, request, *args, **kwargs):
        chatroom = self.get_chatroom_from_request(request)
        serializer = MessageSerializer(
            self.get_queryset(queryset=chatroom.messages.all()),
            many = True,
            context = {'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_message(self, request, *args, **kwargs):
        serializer = ChatroomMessageSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer.validated_data['chatroom'] = chatroom
        if isinstance(request.user, User):
            serializer.validated_data['sender'] = request.user
        serializer.save()
        return Response(
            ChatroomMessageSerialzier(chatroom.messages.all(), many=True).data,
            status=status.HTTP_201_CREATED,
        )