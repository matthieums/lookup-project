from django.core.management.base import BaseCommand
from ...tests.factories import SchoolFactory, CourseFactory, TeacherFactory, StudentFactory

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        NUMBER_OF_SAMPLES = 10
        SAMPLED_DATA = ['school', 'teacher', 'course']

        for _ in range(NUMBER_OF_SAMPLES + 1):
            print(f'execution number {_}')
            school = SchoolFactory()
            teacher = TeacherFactory()
            student = StudentFactory()
            course = CourseFactory(place=school)

            course.teachers.add(teacher)

            course.save()
            teacher.save()
            student.save()
            school.save()

        self.stdout.write(self.style.SUCCESS(
            f'Database populated with {NUMBER_OF_SAMPLES} of each {", ".join(SAMPLED_DATA)}'
            ))
