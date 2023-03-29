from django.test import TestCase

from accounts.models import CustomUser as User

class CreateUserMixin:

    def create_user(self, username=None, email=None, password=None):
        user = User.objects.create(
            username = username if username is not None else 'test-user',
            email = email if email is not None else 'user@testsuit.com',
            password = password if password is not None else 'test$psswd',
        )
        return user

class TestUser(CreateUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user(self):
        self.assertEqual(User.objects.filter(username='test-user').exists(), True)
        self.assertEqual(User.objects.get(username='test-user').email, self.user.email)
        self.assertEqual(User.objects.get(username='test-user').password, self.user.password)
