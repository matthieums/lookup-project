from django.test import TestCase
from django.urls import reverse
from .factories import SchoolFactory, CourseFactory, StudentFactory

class LoginTestCase(TestCase):
    def setUp(self):
        """Set up a user to be used in the login tests."""
        self.user = StudentFactory(username='testuser', password='testpass')
        self.login_url = reverse('login')

    def test_login_success(self):
        """Test that a user can log in with the correct credentials."""
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        
        self.assertRedirects(response, '/') 
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertEqual(self.client.session['_auth_user_backend'], 'django.contrib.auth.backends.ModelBackend')