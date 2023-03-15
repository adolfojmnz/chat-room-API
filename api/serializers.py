from rest_framework import serializers

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Chat, Topic
from msg.models import Message, Files


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'birthdate' 'last_login', 'date_joined']
        read_only = ['bio', 'last_login', 'date_joined']


class ChatroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatroom
        fields = ['name', 'description', 'creation_date', 'public', 'min_age_required', 'topics', 'participants', 'messages', 'files']
        read_only = ['creation_date', 'topics', 'participants' 'messages', 'files']


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['participants', 'messages', 'files']
        read_only = ['messages', 'files']

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['name', 'description']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender', 'body']


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = ['sender', 'file', 'type_name', 'max_size_kbytes']
