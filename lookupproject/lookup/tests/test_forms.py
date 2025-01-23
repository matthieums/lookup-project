from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .factories import SchoolFactory, CourseFactory, TeacherFactory
from lookup.models import Course


class CourseFormTestCase(TestCase):
    
    def setUp(self):
        """Set up test data including a user and a school."""
        self.user = TeacherFactory(username='testuser', password='testpass')
        self.school = SchoolFactory()
        self.url = reverse('contact') 

    def test_form_submission_valid(self):
        """Test the form submission with valid data"""

        self.client.login(username='testuser', password='testpass')

        form_data = {
            'name': 'Test Course',
            'description': 'A course description.',
            'place': self.school.id,
            'teachers': self.user.id,
            'schedule': '2025-01-01T12:00:00Z',
            'target_audience': 'ANYONE',
            'discipline': 'CS',
            'online': True,
            'created_by': self.user.id,
        }

        # Send the POST request to the form submission URL
        response = self.client.post(self.url, form_data)

        # Check that the response redirects to the expected URL
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertRedirects(response, '/success')  # Replace with the actual redirect URL

        # Check that the Course has been created
        self.assertTrue(Course.objects.filter(name='Test Course').exists())
        
    def test_form_submission_invalid(self):
        """Test the form submission with invalid data"""
        # Login the user
        self.client.login(username='testuser', password='testpass')
        
        # Send invalid data (e.g., missing required field)
        invalid_form_data = {
            'name': '',  # Name is required, so this will be invalid
            'description': 'A course description.',
            'place': self.school.id,
            'teachers': self.user.id,
            'schedule': '2025-01-01T12:00:00Z',
            'target_audience': 'ANYONE',
            'discipline': 'CS',
            'online': True,
            'created_by': self.user.id,
        }
        
        # Send the POST request with invalid data
        response = self.client.post(self.url, invalid_form_data)

        # Check that the form is re-rendered with errors (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Check that the form errors are present (e.g., 'name' field is required)
        self.assertFormError(response, 'form', 'name', 'This field is required.')