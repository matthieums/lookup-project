from django.test import TestCase

class test_views(TestCase):
    def test_index(self):
        """
        Check if index returns status code 200
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    