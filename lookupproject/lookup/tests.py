from django.test import TestCase

# Tests to check if the views respond properly
class test_views(TestCase):
    """Check that all views respond properly"""

    def test_index_response(self):
        """Check that index returns status code 200"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_response(self):
        """Check that about returns status code 200"""
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_classes_response(self):
        """Check that classes returns status code 200"""
        response = self.client.get("/classes")
        self.assertEqual(response.status_code, 200)

    def test_schools_response(self):
        """Check that schools returns status code 200"""
        response = self.client.get("/schools")
        self.assertEqual(response.status_code, 200)

    def test_contact_response(self):
        """Check that contact returns status code 200"""
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)

    def test_about_response(self):
        """Check that teachers returns status code 200"""
        response = self.client.get("/teachers")
        self.assertEqual(response.status_code, 200)