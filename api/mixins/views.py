from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic

from api.serializers import UserSerializer


class GetChatroomMixin:

    def get_chatroom_from_request(self, request):
        chatroom_id = request.parser_context['kwargs'].get('pk')
        try:
            return Chatroom.objects.get(pk=chatroom_id)
        except Chatroom.DoesNotExist:
            return None


class ChatroomTopicHelperMixin:

    def get_topic_from_request(self, request):
        topic_id = request.data.get('id')
        try:
            return Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return None


class ChatroomParticipantsHelperMixin(GetChatroomMixin):

    def get_participant(self, request):
        participant_id = request.data.get('id')
        if participant_id is not None:
            try:
                return User.objects.get(pk=participant_id)
            except User.DoesNotExist:
                return None
        return None

    def list_participants(self, request):
        chatroom = self.get_chatroom_from_request(request)
        if isinstance(chatroom, Chatroom):
            serializer = UserSerializer(chatroom.participants.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Object not found!'}, status=status.HTTP_404_NOT_FOUND)

    def perform_add_or_delete_participant(self, request):
        chatroom = self.get_chatroom_from_request(request)
        participant = self.get_participant(request)
        if not isinstance(chatroom, Chatroom):
            return Response({'Bad Request': 'Chatroom not found!'}, status=status.HTTP_404_NOT_FOUND)
        if not isinstance(participant, User):
            return Response({'Bad Request': 'Participant not found!'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            chatroom.participants.add(participant)
        if request.method == 'DELETE':
            chatroom.participants.remove(participant)
        chatroom.save()
        serializer = UserSerializer(chatroom.participants.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
