import random
from django.core.management.base import BaseCommand
from ...tests.factories import (SchoolFactory, TeacherFactory, StudentFactory,
                                DanceCourses, MusicCourses, DramaCourses
                                )

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        NUMBER_OF_SAMPLES = 10

        schools = SchoolFactory.create_batch(NUMBER_OF_SAMPLES)
        teachers = TeacherFactory.create_batch(NUMBER_OF_SAMPLES)
        students = StudentFactory.create_batch(NUMBER_OF_SAMPLES)

        dance_courses = [DanceCourses.create(place=schools[i], created_by=random.choice(teachers)) for i in range(NUMBER_OF_SAMPLES)]
        drama_courses = [DramaCourses.create(place=schools[i], created_by=random.choice(teachers)) for i in range(NUMBER_OF_SAMPLES)]
        music_courses = [MusicCourses.create(place=schools[i], created_by=random.choice(teachers)) for i in range(NUMBER_OF_SAMPLES)]

        for course_list in [dance_courses, drama_courses, music_courses]:
            for course in course_list:
                course.teachers.add(course.created_by)

        self.stdout.write(self.style.SUCCESS(
            f"Database populated with {NUMBER_OF_SAMPLES} schools, teachers, students, and courses."
        ))
