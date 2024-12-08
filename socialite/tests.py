from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSignalTests(TestCase):
    def setUp(self):
        # Create a user instance
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_user_profile_created_on_user_creation(self):
        """
        Test that a UserProfile instance is automatically created
        when a new User instance is created.
        """
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_user_profile_saved_on_user_save(self):
        """
        Test that the UserProfile instance is saved when the User instance is saved.
        """
        self.user.first_name = "Updated Name"
        self.user.save()

        # Reload the profile from the database
        self.user.profile.refresh_from_db()

        # Verify profile is still linked
        self.assertEqual(self.user.profile.user, self.user)

    def test_user_profile_default_fields(self):
        """
        Test the default values of UserProfile fields.
        """
        profile = self.user.profile
        self.assertEqual(profile.bio, "")
        self.assertFalse(profile.profile_picture.name)

class UserProfileModelTests(TestCase):
    def test_profile_creation_with_custom_bio(self):
        """
        Test that we can customize the UserProfile fields after creation.
        """
        user = User.objects.create_user(username="anotheruser", password="anotherpassword")
        user.profile.bio = "This is a test bio."
        user.profile.save()

        # Reload from the database
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.bio, "This is a test bio.")
