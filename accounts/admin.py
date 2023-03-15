from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['first_name', 'last_name', 'username', 'email', 'password']

admin.site.register(CustomUser)