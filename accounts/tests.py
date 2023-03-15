from django.test import TestCase

from accounts.models import CustomUser as User

class CreateTestUserMixin:

    def create_test_user(self):
        user = User.objects.create(
            username = 'test-user',
            email = 'user@testsuit.com',
            password = 'test$psswd',
        )
        return user


class TestUser(CreateTestUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_test_user()
        self.user.save()

    def test_user(self):
        self.assertEqual(User.objects.filter(username='test-user').exists(), True)
        self.assertEqual(User.objects.get(username='test-user').email, self.user.email)
        self.assertEqual(User.objects.get(username='test-user').password, self.user.password)