from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@email.com', password='password')

        # Check if user is created
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Check if user is saved to database with correct values
        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email='')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='123')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='superuser@email.com', password='password')

        # Check if superuser is created
        self.assertEqual(admin_user.email, 'superuser@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class CustomUserModelTests(TestCase):

    def test_user_slug_is_unique(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@email.com', password='password')
        user2 = User.objects.create_user(email='user2@gmail.com', password='password')
        self.assertNotEqual(user.slug, user2.slug)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='user@email.com', slug='user-slug', password='password')
            User.objects.create_user(email='user2@gmail.com', slug='user-slug', password='password')

    def test__str__(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@email.com', password='password')
        self.assertEqual(user.__str__(), user.email)

    def test_user_slug_is_generated_if_blank(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@email.com', password='password')
        self.assertNotEqual(user.slug, '')

    def test_user_slug_is_not_overwritten(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@email.com', password='password', slug='weird-slug')
        self.assertEqual(user.slug, 'weird-slug')
