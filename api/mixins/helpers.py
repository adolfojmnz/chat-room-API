from chatrooms.models import Message, Topic, Chatroom


class GetModelObjectFromRequestMixin:

    def get_model_object_from_request(self, model_instance, request):
        object_id = request.parser_context['kwargs'].get('pk')
        try:
            return model_instance.objects.get(pk=object_id)
        except model_instance.DoesNotExist:
            return None


class UserMixin:

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else super().get_queryset()

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


class TopicMixin(GetModelObjectFromRequestMixin):

    def get_topic_from_request(self, request):
        return self.get_model_object_from_request(Topic, request)

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else super().get_queryset()

        name = self.request.query_params.get('name')
        if name is not None:
            self.queryset =  self.queryset.filter(name__icontains=name)
        description = self.request.query_params.get('description')
        if description is not None:
            self.queryset = self.queryset.filter(description__icontains=description)

        return self.queryset


class MessageMixin(GetModelObjectFromRequestMixin):

    def get_message_from_request(self, request):
        return self.get_model_object_from_request(Message, request)

    def get_queryset(self, queryset=None):
        self.queryset = queryset if queryset is not None else super().get_queryset()

        body = self.request.query_params.get('body')
        if body is not None:
            self.queryset = self.queryset.filter(body__icontains=body).distinct()
        sender = self.request.query_params.get('sender')
        if sender is not None:
            self.queryset = self.queryset.filter(sender__username=sender)

        return self.queryset


class ChatroomMixin(GetModelObjectFromRequestMixin):

    def get_chatroom_from_request(self, request):
        return self.get_model_object_from_request(Chatroom, request)

    def get_queryset(self):
        self.queryset = self.queryset.filter(public=True)

        name = self.request.query_params.get('name')
        topic = self.request.query_params.get('topic')
        if name is not None:
            self.queryset = self.queryset.filter(name__icontains=name).distinct()
        if topic is not None:
            self.queryset = self.queryset.filter(topics__name__icontains=topic).distinct()
        return self.queryset
