from django.test import TestCase

from accounts.models import CustomUser as User, ContactBook

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

class CreateContactBookMixin:

    def create_contact_book(self):
        contact_book = ContactBook.objects.create(
            book_owner = self.user,
        )
        contact_book.contacts.set(self.user_list)
        return contact_book


class TestUser(CreateUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()

    def test_user(self):
        self.assertEqual(User.objects.filter(username='test-user').exists(), True)
        self.assertEqual(User.objects.get(username='test-user').email, self.user.email)
        self.assertEqual(User.objects.get(username='test-user').password, self.user.password)


class TestContactBook(CreateContactBookMixin, CreateUserMixin, TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.user_list = self.create_user_list()
        self.contact_book = self.create_contact_book()

    def test_contact_book(self):
        self.assertTrue(isinstance(self.contact_book, ContactBook))
        self.assertTrue(isinstance(self.contact_book.book_owner, User))
        self.assertEqual(self.contact_book.book_owner, self.user)
        self.assertTrue(self.contact_book.contacts.count() > 0)
