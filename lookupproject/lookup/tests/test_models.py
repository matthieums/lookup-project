from django.test import TestCase
from lookup.models import School, Course, Teacher
from lookup.models import MUSIC, ELDERLY
from datetime import datetime
from django.utils.timezone import make_aware


class SchoolTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        School.objects.create(
            name='testschool',
            location='testlocation',
            contact='test@test.com',
            website='www.test.com'
        )

    def testSchoolObjectCreation(self):
        school = School.objects.get(name='testschool')
        self.assertEqual(school.name, 'testschool')
        self.assertEqual(school.location, 'testlocation')
        self.assertEqual(school.contact, 'test@test.com')
        self.assertEqual(school.website, 'www.test.com')


class TeacherTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.school = School.objects.create(
            name='testschool',
            location='testlocation',
            contact='test@test.com',
            website='www.test.com'
        )
        cls.teacher = Teacher.objects.create(
            name='testname',
            last_name='testlastname',
            disciplines=MUSIC,
            mailaddress='test@test.com',
            phone_number='+55555555555555'
        )
        # Assign ManyToManyField relationship using set()
        cls.teacher.schools.set([cls.school])

    def testTeacherObjectCreation(self):
        teacher = Teacher.objects.get(name='testname')
        self.assertEqual(teacher.name, 'testname')
        self.assertEqual(teacher.last_name, 'testlastname')
        self.assertIn(self.school, teacher.schools.all())
        self.assertEqual(teacher.disciplines, MUSIC)
        self.assertEqual(teacher.mailaddress, 'test@test.com')
        self.assertEqual(teacher.phone_number, '+55555555555555')


class CourseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.school = School.objects.create(
            name='testschool',
            location='testlocation',
            contact='test@test.com',
            website='www.test.com'
        )
        cls.teacher = Teacher.objects.create(
            name='testname',
            last_name='testlastname',
            disciplines=MUSIC,
            mailaddress='test@test.com',
            phone_number='+55555555555555'
        )

        # Assign many to many relationship
        cls.teacher.schools.set([cls.school])

        cls.test_schedule = make_aware(datetime(2024, 12, 25, 10, 0, 0))

        cls.course = Course.objects.create(
            name='testcourse',
            description='testdescription',
            place=cls.school,
            schedule=cls.test_schedule,
            target_audience=ELDERLY,
            discipline=MUSIC,
            online=False
        )

        # Assign many to many relationship
        cls.course.teachers.set([cls.teacher])

    def testCourseObjectCreation(self):
        course = Course.objects.get(name='testcourse')
        self.assertEqual(course.name, 'testcourse')
        self.assertEqual(course.description, 'testdescription')
        self.assertEqual(course.place, self.school)
        self.assertIn(self.teacher, course.teachers.all())
        self.assertEqual(course.schedule, self.test_schedule)
        self.assertEqual(course.target_audience, ELDERLY)
        self.assertEqual(course.discipline, MUSIC)
        self.assertFalse(course.online)
