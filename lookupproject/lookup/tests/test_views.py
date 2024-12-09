from django.test import TestCase


# Tests to check if the views respond properly
class test_views(TestCase):
    """Check that all views respond properly"""

    def test_index_response(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_response(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_courses_response(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 200)

    def test_schools_response(self):
        response = self.client.get("/schools")
        self.assertEqual(response.status_code, 200)

    def test_contact_response(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
