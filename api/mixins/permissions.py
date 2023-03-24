from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)

from api.mixins.views import (
    UserMixin,
    MessageMixin,
    ChatroomMixin,
)

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DANGEROUS_METHODS = ['PUT', 'PATCH', 'DELETE']


class IsChatroomAdmin(BasePermission, ChatroomMixin):
    """ Permission Class to be used with ChatPermissionsMixin """

    def has_permission(self, request, view):
        user = request.user
        chatroom = self.get_chatroom_from_request(request)
        user_is_chatroom_admin = user.is_active and chatroom.admins.filter(username=user.username).exists()
        user_admin = user.is_staff or user.is_superuser
        return bool(user_is_chatroom_admin or user_admin)


class UserPermissionsMixin:

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method in ['POST']:
            self.permission_classes = []
        elif self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in DANGEROUS_METHODS:
            if self.request.user.pk == self.request.parser_context['kwargs'].get('pk'):
                self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class MessageListPermissionsMixin:

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class MessageDetailPermissionsMixin(MessageMixin):

    def user_sent_message(self, request):
        user = request.user
        message = self.get_message_from_request(request)
        if message.sender.pk == user.pk:
            return True
        return False

    def are_user_and_message_in_same_chatroom(self, request):
        user = request.user
        message = self.get_message_from_request(request)
        if message.chatroom.participants.filter(pk=user.pk):
            return True
        return False

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method in SAFE_METHODS:
            if self.are_user_and_message_in_same_chatroom(self.request):
                self.permission_classes = [IsAuthenticated]
        if self.request.method in DANGEROUS_METHODS:
            if self.user_sent_message(self.request):
                self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ChatroomListPermissionsMixin:

    def get_permissions(self):
        self.permission_classes = [IsChatroomAdmin]
        if self.request.method in ['POST']:
            self.permission_classes  = [IsAuthenticated]
        elif self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ChatroomDetailPermissionsMixin(ChatroomMixin, UserMixin):

    def user_in_chatroom(self):
        user = self.request.user
        chatroom = self.get_chatroom_from_request(self.request)
        if chatroom.participants.filter(pk=user.pk).exists():
            return True
        return False

    def requested_chatroom_is_public(self):
        chatroom = self.get_chatroom_from_request(self.request)
        return chatroom.public

    def get_permissions(self):
        self.permission_classes = [IsChatroomAdmin]
        if self.request.method in SAFE_METHODS:
            if self.requested_chatroom_is_public():
                self.permission_classes = [IsAuthenticated]
        elif self.request.method in DANGEROUS_METHODS:
            self.permission_classes = [IsChatroomAdmin]
        return super().get_permissions()
