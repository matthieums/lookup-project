from django.test import TestCase
from django.contrib.gis.geos import Point
from lookup.models import School
import random
from .factories import (
    SchoolFactory,
    TeacherFactory,
    StudentFactory,
    CourseFactory
    )


class SchoolModelTest(TestCase):

    # def test_unique_contact_constraint(self):
    """Test that 'contact' must be unique."""

    def test_point_field(self):
        """Test handling of PointField data."""
        school = SchoolFactory()
        self.assertIsInstance(school.coordinates, Point)
        self.assertGreaterEqual(school.coordinates.x, -180.0)
        self.assertLessEqual(school.coordinates.x, 180.0)
        self.assertGreaterEqual(school.coordinates.y, -90.0)
        self.assertLessEqual(school.coordinates.y, 90.0)

        # Test nullable coordinates
        school_no_coords = School.objects.create(
            name="School Without Coordinates",
            location="Somewhere",
            contact="contact@example.com",
        )
        self.assertIsNone(school_no_coords.coordinates)


class SchoolRandomCoordinatesTest(TestCase):
    def test_random_coordinates(self):
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        coordinates = Point(longitude, latitude)

        school = School.objects.create(
            name="Test Random School",
            location="Test Location",
            coordinates=coordinates,
            contact="random_test_school@example.com",
            website="https://testschool.example.com",
        )

        self.assertAlmostEqual(school.coordinates.x, longitude, places=6)
        self.assertAlmostEqual(school.coordinates.y, latitude, places=6)
