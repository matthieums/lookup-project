from django.core.management.base import BaseCommand
from ...tests.factories import SchoolFactory, CourseFactory, TeacherFactory


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        school = SchoolFactory()
        teacher = TeacherFactory()
        course = CourseFactory(place=school)

        teacher.schools.add(school)
        course.teachers.add(teacher)
        course.save()

        self.stdout.write(self.style.SUCCESS(
            'Database populated with sample data.'
            ))
