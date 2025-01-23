from django.test import TestCase
from django.urls import reverse
from lookup.models import CustomUser

# URLS
INDEX = reverse('index')
ABOUT = reverse('about')
TEACHERS = reverse('teachers')
SCHOOLS = reverse('schools')
CREATE_COURSE = reverse('create_course')
CREATE_SCHOOL = reverse('new_school')
MY_COURSES = reverse('my_courses')
REGISTER = reverse('register')
SUCCESS = reverse('success')


# Tests to check if the views respond properly
class TestViews(TestCase):
    """Check that all views respond with status code 200"""
    def test_index_response(self):
        response = self.client.get(INDEX)
        self.assertEqual(response.status_code, 200)

    def test_about_response(self):
        response = self.client.get(ABOUT)
        self.assertEqual(response.status_code, 200)

    def test_teachers_response(self):
        response = self.client.get(TEACHERS)
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
    """Check that restricted views redirect unauthenticated users"""
    def test_unauthenticated_new_course_response(self):
        response = self.client.get(CREATE_COURSE)
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_new_school_response(self):
        response = self.client.get(CREATE_SCHOOL)
        self.assertEqual(response.status_code, 302)


class TestTeacherAndStudentRestrictions(TestCase):
    """Check that students and teachers have different authorizations"""
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student_user',
            password='password123',
            role='student'
            )
        self.teacher = CustomUser.objects.create_user(
            username='teacher_user',
            password='password123',
            role='teacher'
            )

    def login_and_check_status(self, username, password, url,expected_status_code):
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status_code)

    def test_student_create_course_response(self):
        self.login_and_check_status(
            'student_user',
            'password123',
            CREATE_COURSE,
            403
            )

    def test_teacher_create_course_response(self):
        self.login_and_check_status(
            'teacher_user',
            'password123',
            CREATE_COURSE,
            200
            )

    def test_student_create_school_response(self):
        self.login_and_check_status(
            'student_user',
            'password123',
            CREATE_COURSE,
            403
            )

    def test_teacher_create_school_response(self):
        self.login_and_check_status(
            'teacher_user',
            'password123',
            CREATE_COURSE,
            200
            )


class TestApiDependentViews(TestCase):
    """Check views requiring arguments in their URL"""
        # new_school
        # teacher_profile
        # school_profile

    # API dependant
    # my_courses

    # delete_course
    # getTeacher
    # getCourse
    # getSchool
    # get_nearby_locations
    # participants
