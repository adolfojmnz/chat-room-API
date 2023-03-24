from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)

from api.mixins.views import (
    ChatroomMixin,
    UserMixin,
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
