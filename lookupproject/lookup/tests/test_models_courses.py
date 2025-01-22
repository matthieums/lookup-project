from django.test import TestCase
from .factories import SchoolFactory, TeacherFactory, StudentFactory, CourseFactory

class EnrollTestCase(TestCase):
    def setUp(self):
        self.user = StudentFactory(username='testuser', password='testpass')
        self.school = SchoolFactory()
        self.course = CourseFactory(name='Test Course', capacity=1, place=self.school)

    def test_enroll_success(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/enroll/{self.course.id}')
        self.assertRedirects(response, '/success')
        self.assertIn(self.user, self.course.students.all())

    def test_enroll_full(self):
        self.client.login(username='testuser', password='testpass')
        another_user = StudentFactory(username='otheruser', password='testpass')
        self.course.students.add(another_user)

        response = self.client.post(f'/enroll/{self.course.id}/')
        self.assertEqual(response.status_code, 404)
