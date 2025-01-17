from django.test import TestCase
from .factories import SchoolFactory, TeacherFactory, StudentFactory, CourseFactory
from django.contrib.gis.geos import Point

class SchoolFactoryTestClass(TestCase):
        
    def test_school_creation_with_factory(self):
            school = SchoolFactory()
            self.assertIsNotNone(school.id)
            self.assertIsInstance(school.coordinates, Point)
            self.assertGreaterEqual(len(school.name), 1)
            self.assertIn("@", school.contact)

    def test_bulk_school_creation_with_factory(self):
        schools = SchoolFactory.create_batch(10)
        self.assertEqual(len(schools), 10)
        for school in schools:
            self.assertIsNotNone(school.id)
            self.assertIsInstance(school.coordinates, Point)


# class TeacherFactoryTestClass(TestCase):


# class StudentFactoryTestClass(TestCase):


# class CourseFactoryTestClass(TestCase):