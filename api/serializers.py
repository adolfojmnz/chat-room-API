from rest_framework import serializers

from accounts.models import CustomUser as User
from chatrooms.models import Chatroom, Topic, ChatroomMessage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'birthdate', 'last_login', 'date_joined']
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


class ChatroomMessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ChatroomMessage
        fields = ['chatroom', 'sender', 'body']
        extra_kwargs = {
            'chatroom': {'view_name': 'api:chatroom-detail'},
            'sender': {'view_name': 'api:user-detail'},
        }


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['name', 'description']
