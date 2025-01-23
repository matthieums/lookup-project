from django.test import TestCase
from django.urls import reverse
from lookup.models import CustomUser

# URLS
INDEX = reverse('index')
ABOUT = reverse('about')
COURSES = reverse('courses')
TEACHERS = reverse('teachers')
SCHOOLS = reverse('schools')
CREATE_COURSE = reverse('create_course')
CREATE_SCHOOL = reverse('new_school')
MY_COURSES = reverse('my_courses')
REGISTER = reverse('register')
SUCCESS = reverse('success')


# Tests to check if the views respond properly
class TestViews(TestCase):
    """Check that all views respond properly"""
    def test_index_response(self):
        response = self.client.get(INDEX)
        self.assertEqual(response.status_code, 200)

    def test_about_response(self):
        response = self.client.get(ABOUT)
        self.assertEqual(response.status_code, 200)

    def test_courses_response(self):
        response = self.client.get(COURSES)
        self.assertEqual(response.status_code, 200)

    def test_schools_response(self):
        response = self.client.get(SCHOOLS)
        self.assertEqual(response.status_code, 200)

    def test_register_response(self):
        response = self.client.get(REGISTER)
        self.assertEqual(response.status_code, 200)

    def test_success_response(self):
        response = self.client.get(SUCCESS)
        self.assertEqual(response.status_code, 200)


class TestUnauthenticatedLoginRequired(TestCase):
    """Check that some views are restricted to logged in users"""

    def test_unauthenticated_new_course_response(self):
        response = self.client.get(CREATE_COURSE)
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_new_school_response(self):
        response = self.client.get(CREATE_SCHOOL)
        self.assertEqual(response.status_code, 302)


class TestAuthenticatedLoginRequired(TestCase):
    """Check that logged in users can access restricted views"""
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123'
            )

    def test_authenticated_create_course_response(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(CREATE_COURSE)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_create_school_response(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(CREATE_SCHOOL)
        self.assertEqual(response.status_code, 200)

        # register
        # teachers
        # new_school
        # teacher_profile
        # school_profile
        # Success
        # Enroll


    # API dependant
    # my_courses

    # delete_course
    # getTeacher
    # getCourse
    # getSchool
    # get_nearby_locations
    # participants
