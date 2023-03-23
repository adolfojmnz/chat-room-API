from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)


class UserPermissionsMixin:

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method in ['POST']:
            self.permission_classes = []
        elif self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PATCH', 'PUT', 'DELETE']:
            if self.request.user.pk == self.request.parser_context['kwargs'].get('pk'):
                self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
