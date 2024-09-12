from django.test import TestCase

class test_views(TestCase):
    """Check that all views respond properly"""

    def test_index_response(self):
        """Check that index returns status code 200"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    