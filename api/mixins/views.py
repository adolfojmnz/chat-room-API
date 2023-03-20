from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic

from api.serializers import (
    UserSerializer,
    TopicSerializer,
)


class GetChatroomMixin:

    def get_chatroom_from_request(self, request):
        chatroom_id = request.parser_context['kwargs'].get('pk')
        try:
            return Chatroom.objects.get(pk=chatroom_id)
        except Chatroom.DoesNotExist:
            return None


class ChatroomTopicHelperMixin(GetChatroomMixin):

    def get_topic_from_request(self, request):
        topic_id = request.data.get('id')
        try:
            return Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return None

    def list_topics(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer = TopicSerializer(chatroom.topics.all(), many=True)
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


class ChatroomParticipantsHelperMixin(GetChatroomMixin):

    def get_participant_from_request(self, request):
        participant_id = request.data.get('id')
        try:
            return User.objects.get(pk=participant_id)
        except User.DoesNotExist:
            return None

    def list_participants(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer = UserSerializer(chatroom.participants.all(), many=True)
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
