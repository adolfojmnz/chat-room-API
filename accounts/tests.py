from django.test import TestCase

from accounts.models import CustomUser as User


class TestUser(TestCase):

    def setUp(self):
        user = User.objects.create(
            username = 'test-user',
            email = 'user@testsuit.com',
            password = 'test$psswd',
        )
        user.save()
        self.user = user

    def test_user(self):
        self.assertEqual(User.objects.filter(username='test-user').exists(), True)
        self.assertEqual(User.objects.get(username='test-user').email, self.user.email)
        self.assertEqual(User.objects.get(username='test-user').password, self.user.password)