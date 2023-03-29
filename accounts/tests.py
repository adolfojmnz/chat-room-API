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

    def create_user_list(self):
        user_list = []
        for username in ['test-user2', 'test-user3', 'test-user4']:
            user_list.append(self.create_user(username=username))
        return user_list

class TestUser(CreateUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.user_list = self.create_user_list()
        self.user.friends.add(self.user.pk)
        self.user.friends.set(self.user_list)
        self.user.clean_friends()

    def test_user(self):
        self.assertEqual(User.objects.filter(username='test-user').exists(), True)
        self.assertEqual(User.objects.get(username='test-user').email, self.user.email)
        self.assertEqual(User.objects.get(username='test-user').password, self.user.password)

    def test_user_friends(self):
        self.assertTrue(User.objects.get(username=self.user.username).friends.count() > 0)
        self.assertFalse(User.objects.get(username=self.user.username).friends.filter(pk=self.user.pk).exists())
