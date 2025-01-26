from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from .factories import SchoolFactory, CourseFactory, TeacherFactory
from django.contrib.gis.geos import Point
import urllib.parse
from django.urls import reverse


# TO-DO:
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

    def test_01_filter_by_radius(self):
        """Test that the view correctly returns nearby schools based on
        coordinates and radius"""

        url = reverse('getCourse')
        params = {
            'radius': 10,
            'user_lon': -71.1167,
            'user_lat': 42.3770
        }
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)

        for course in response.data:
            school_location = course['place']
            distance = school_location.distance(
                Point(float(params['user_lon']),
                float(params['user_lat']))
            )
            self.assertLessEqual(distance, 10)

    def test_02_missing_fields(self):
        """Test that the view returns a 400 error when required fields are missing"""
        response = self.client.get(
            '/courses/get/',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_03_invalid_coordinates(self):
        """Test that the view returns a 400 error when coordinates are invalid"""
        params = {'user_lat': 'invalid', 'user_lon': 'invalid', 'radius': 10}
        query_url = self.build_query_string(params)
        response = self.client.get(
            f'/courses/get/{query_url}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class TestCourseFiltering(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.teacher = TeacherFactory()
        self.school_1 = SchoolFactory(coordinates=Point(-71.1167, 42.3770))
        self.school_2 = SchoolFactory(coordinates=Point(-71.1067, 42.3870))
        self.school_3 = SchoolFactory(coordinates=Point(-2, 10))

        self.course_1 = CourseFactory(place=self.school_1, created_by=self.teacher)
        self.course_2 = CourseFactory(place=self.school_2, created_by=self.teacher)
        self.course_3 = CourseFactory(name='invalid', place=self.school_3, created_by=self.teacher)

    def test_01_filter_by_created_by(self):
        url = reverse('getCourse')
        params = {'created_by': self.teacher.id}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        for course in response.data:
            self.assertEqual(course['created_by'], self.teacher.id)

    def test_02_filter_by_discipline(self):
        url = reverse('getCourse')
        params = {'discipline': self.course_1.discipline}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        for course in response.data:
            self.assertEqual(course['discipline'], self.course_1.discipline)

    def test_03_filter_by_age_group(self):
        url = reverse('getCourse')
        params = {'age_group': self.course_1.target_audience}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        for course in response.data:
            self.assertEqual(course['target_audience'], self.course_1.target_audience)

    def test_04_filter_by_created_by_and_discipline(self):
        url = reverse('getCourse')
        params = {'created_by': self.teacher.id, 'discipline': self.course_1.discipline}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        for course in response.data:
            self.assertEqual(course['created_by'], self.teacher.id)
            self.assertEqual(course['discipline'], self.course_1.discipline)
