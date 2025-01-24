from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from .factories import SchoolFactory, CourseFactory, TeacherFactory
from django.contrib.gis.geos import Point
import urllib.parse

# TO-DO:
# Test serializers
# Test missing queryparams. What should it return in my view?
# Test filter combination
# Test radius
# Test user geographic position

class TestGetNearbyLocations(APITestCase):
    def setUp(self):
        """Setup using factories to create schools with random coordinates"""
        self.client = APIClient()

        self.teacher = TeacherFactory()
        self.school_1 = SchoolFactory(coordinates=Point(-71.1167, 42.3770))
        self.school_2 = SchoolFactory(coordinates=Point(-71.1067, 42.3870))
        self.school_3 = SchoolFactory(coordinates=Point(-2, 10))

        self.course_1 = CourseFactory(place=self.school_1, created_by=self.teacher)
        self.course_2 = CourseFactory(place=self.school_2, created_by=self.teacher)
        self.course_3 = CourseFactory(name='invalid', place=self.school_3, created_by=self.teacher)

    # Helper function
    def build_query_string(self, params):

        filtered_params = {
            k: v for k, v in params.items() if v is not None and v != ""
            }

        query_string = urllib.parse.urlencode(filtered_params)

        fetch_url = f"?{query_string}"

        return fetch_url
    
    def test_01_get_nearby_locations(self):
        """Test that the view correctly returns nearby schools based on
        coordinates and radius"""

        user_lat = 42.3770
        user_lon = -71.1167
        radius = 5

        params = {
            "radius": radius,
            "user_lon": user_lon,
            "user_lat": user_lat
        }

        query_url = self.build_query_string(params)

        response = self.client.get(
            f'/courses/get/{query_url}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        nearby_courses = response.json()
        self.assertEqual(len(nearby_courses), 2)
        course_names = [course['name'] for course in nearby_courses]

        self.assertIn(self.course_1.name, course_names)
        self.assertIn(self.course_2.name, course_names)
        self.assertNotIn(self.course_3.name, course_names)

    def test_02_missing_fields(self):
        """Test that the view returns a 400 error when required fields are missing"""
        response = self.client.get(
            '/courses/get/',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_invalid_coordinates(self):
        """Test that the view returns a 400 error when coordinates are invalid"""
        params = {'user_lat': 'invalid', 'user_lon': 'invalid', 'radius': 10}
        query_url = self.build_query_string(params)
        response = self.client.get(
            f'/courses/get/{query_url}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


