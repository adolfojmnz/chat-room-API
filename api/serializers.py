from rest_framework import serializers

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic, Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'bio', 'birthdate', 'last_login', 'date_joined']
        read_only = ['bio', 'last_login', 'date_joined']


class ChatroomSerializer(serializers.ModelSerializer):
    topics = serializers.HyperlinkedRelatedField(
        many = True,
        read_only = True,
        view_name = 'api:topic-detail',
    )
    participants = serializers.HyperlinkedRelatedField(
        many = True,
        read_only = True,
        view_name = 'api:user-detail',
    )

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'description', 'creation_date', 'public', 'min_age_required', 'topics', 'participants']
        read_only = ['creation_date']


class MessageSerializer(serializers.ModelSerializer):
    chatroom = serializers.HyperlinkedRelatedField(
        view_name = 'api:chatroom-detail',
        read_only = True,
    )
    sender = serializers.HyperlinkedRelatedField(
        view_name = 'api:user-detail',
        read_only = True,
    )
    chatroom_id = serializers.IntegerField(write_only=True)
    sender_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'chatroom_id', 'sender', 'sender_id', 'body']


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description']


class ChatroomMessageSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'body']
