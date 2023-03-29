from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    '''
    default fields:
        username, first_name, last_name, email, password, group, user_permissions,
        is_staff, is_active, is_superuser, last_login, date_joined
    '''
    # for further information refer to https://docs.djangoproject.com/en/4.1/ref/contrib/auth/

    # custom fields
    birthdate = models.DateField(auto_now=True)
    bio = models.CharField(default='', max_length=1000)

    def __str__(self):
        return self.username
