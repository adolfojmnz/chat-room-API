from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom

from api.serializers import UserSerializer, ChatroomSerializer


class ChatroomParticipantsHelperMixin:

    def get_chatroom(self, request):
        pk = request.parser_context['kwargs'].get('pk')
        if pk is not None:
            try:
                return Chatroom.objects.get(pk=pk)
            except Chatroom.DoesNotExist:
                return None
        return None

    def get_participant(self, request):
        participant_id = request.data.get('id')
        if participant_id is not None:
            try:
                return User.objects.get(pk=participant_id)
            except User.DoesNotExist:
                return None
        return None

    def list_participants(self, request):
        chatroom = self.get_chatroom(request)
        if isinstance(chatroom, Chatroom):
            serializer = UserSerializer(chatroom.participants.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Object not found!'}, status=status.HTTP_404_NOT_FOUND)

    def perform_add_or_delete_participant(self, request):
        chatroom = self.get_chatroom(request)
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
