from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from .factories import SchoolFactory
from django.contrib.gis.geos import Point


class TestGetNearbyLocations(APITestCase):
    
    def setUp(self):
        """Setup using factories to create schools with random coordinates"""
        self.client = APIClient()

        self.school_1 = SchoolFactory(coordinates=Point(-71.1167, 42.3770))
        self.school_2 = SchoolFactory(coordinates=Point(-71.1067, 42.3870))
        self.school_3 = SchoolFactory(coordinates=Point(-72.1167, 42.4770))

    def test_missing_fields(self):
        """Test that the view returns a 400 error when required fields are missing."""
        response = self.client.post(
            "/geoschool",  # URL to your endpoint
            data={},  # No data sent
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Missing required fields.")

    def test_get_nearby_locations(self):
        """Test that the view correctly returns nearby schools based on coordinates and radius"""

        user_lat = 42.3770
        user_lon = -71.1167
        radius = 5

        response = self.client.post(
            '/geoschool',
            data={'user_lat': user_lat, 'user_lon': user_lon, 'radius': radius}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        nearby_schools = response.json()
        self.assertEqual(len(nearby_schools), 2)
        school_names = [school['name'] for school in nearby_schools]
        self.assertIn(self.school_1.name, school_names)
        self.assertIn(self.school_2.name, school_names)
        self.assertNotIn(self.school_3.name, school_names)

    def test_missing_fields(self):
        """Test that the view returns a 400 error when required fields are missing"""
        response = self.client.post(
            '/geoschool',
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

    def test_invalid_coordinates(self):
        """Test that the view returns a 400 error when coordinates are invalid"""
        response = self.client.post(
            '/geoschool',
            data={'user_lat': 'invalid', 'user_lon': 'invalid', 'radius': 10}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())