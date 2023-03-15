from rest_framework import serializers

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Chat, Topic, ChatroomMessage, ChatMessage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'birthdate' 'last_login', 'date_joined']
        read_only = ['bio', 'last_login', 'date_joined']


class ChatroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatroom
        fields = ['name', 'description', 'creation_date', 'public', 'min_age_required', 'topics', 'participants']
        read_only = ['creation_date', 'topics', 'participants']


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['participants', 'messages']
        read_only = ['messages', 'files']


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['name', 'description']


class ChatroomMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatroomMessage
        fields = ['chatroom', 'sender', 'body']


class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['chat', 'sender', 'body']