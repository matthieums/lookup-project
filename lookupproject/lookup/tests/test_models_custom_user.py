from django.test import TestCase
from lookup.models import CustomUser
from django.db.utils import DataError


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username='student1',
            password='pass',
            role='student'
            )
        self.teacher_user = CustomUser.objects.create_user(
            username='teacher1',
            password='pass',
            role='teacher'
            )

    def test_default_role(self):
        user = CustomUser.objects.create_user(
            username='default_user',
            password='pass')
        self.assertEqual(user.role, 'student', "Default role should be 'student'")

    def test_role_choices(self):
        with self.assertRaises(DataError):
            CustomUser.objects.create_user(
                username='invalid_user',
                password='pass',
                role='InvalidRole'
                )

    def test_is_student(self):
        self.assertTrue(self.student_user.is_student())
        self.assertFalse(self.teacher_user.is_student())

    def test_is_teacher(self):
        self.assertTrue(self.teacher_user.is_teacher())
        self.assertFalse(self.student_user.is_teacher())

class CustomUserIntegrationTest(TestCase):

    def test_user_crud(self):
        # Create a user
        user = CustomUser.objects.create_user(
            username='test_user',
            password='testpass',
            role='teacher'
            )
        self.assertEqual(CustomUser.objects.count(), 1)

        # Read the user
        retrieved_user = CustomUser.objects.get(username='test_user')
        self.assertEqual(retrieved_user.role, 'teacher')

        # Update the user
        retrieved_user.role = 'student'
        retrieved_user.save()
        self.assertEqual(CustomUser.objects.get(username='test_user').role, 'student')

        # Delete the user
        retrieved_user.delete()
        self.assertEqual(CustomUser.objects.count(), 0)


class CustomUserFunctionalTest(TestCase):

    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username='student1',
            password='pass',
            role='student'
            )
        self.teacher_user = CustomUser.objects.create_user(
            username='teacher1',
            password='pass',
            role='teacher'
            )

    def test_authentication(self):
        # Log in as student
        login = self.client.login(username='student1', password='pass')
        self.assertTrue(login, "Student login failed")

        # Log in as teacher
        login = self.client.login(username='teacher1', password='pass')
        self.assertTrue(login, "Teacher login failed")