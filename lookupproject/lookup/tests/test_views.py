from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from lookup.models import CustomUser
from lookup.tests.factories import SchoolFactory, TeacherFactory, StudentFactory, CourseFactory
from lookup.models import Course

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


# TO-DO: SPLIT UP. TOO LONG.
class TestApiDependentViews(TestCase):
    """Check views requiring arguments in their URL"""

    @classmethod
    def setUpTestData(cls):
        cls.teacher = TeacherFactory(
            username="teacher_user",
            password="password123",
            role="teacher"
            )
        cls.student = StudentFactory(
            username="student_user",
            password="password123",
            role="student"
            )
        cls.school = SchoolFactory()
        cls.course = CourseFactory(place=cls.school, created_by=cls.teacher)
        cls.course.students.add(cls.student)

    def test_01_individual_teacher_view(self):
        url = f"{TEACHERS}/{self.teacher.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.teacher.first_name)

    def test_02_individual_course_view(self):

        url = reverse('course', args=[self.course.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_03_unauthenticated_participants_view(self):
        url = reverse('participants', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_04_authenticated_as_student_participants_view(self):
        self.client.login(username='student_user', password='password123')

        url = reverse('participants', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_05_authenticated_as_creator_participants_view(self):
        self.client.login(username='teacher_user', password='password123')

        url = reverse('participants', args=[self.course.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_06_individual_existing_schools_view(self):
        url = reverse('school_profile', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_08_individual_nonexistent_schools_view(self):
        existing_id = self.school.id
        non_existent_id = existing_id + 1
        url = reverse('school_profile', args=[non_existent_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_09_course_deletion_as_unauthenticated(self):
        url = reverse('delete_course', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_10_course_deletion_as_student(self):
        self.client.login(username='student_user', password='password123')
        url = reverse('delete_course', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_11_course_deletion_as_creator(self):
        self.assertTrue(Course.objects.filter(id=self.course.id).exists())

        self.client.login(username='teacher_user', password='password123')

        url = reverse('delete_course', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())


        # new_school
        # teacher_profile
        # school_profile

    # API dependant
    # my_courses

    # get_nearby_locations

