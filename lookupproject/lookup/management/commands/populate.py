from django.core.management.base import BaseCommand
from ...tests.factories import SchoolFactory, CourseFactory, TeacherFactory


# Pour une raison qui me dépasse, les données dans la boucle ne sont pas recalculées.
# Les factories ne sont pas réexécutées après la première exécution.
class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        NUMBER_OF_SAMPLES = 10
        SAMPLED_DATA = ['school', 'teacher', 'course']

        for _ in range(NUMBER_OF_SAMPLES + 1):
            school = SchoolFactory()
            teacher = TeacherFactory()
            course = CourseFactory(place=school)

            teacher.schools.add(school)
            course.teachers.add(teacher)

            course.save()
            teacher.save()
            school.save()

        self.stdout.write(self.style.SUCCESS(
            f'Database populated with {NUMBER_OF_SAMPLES} of each {", ".join(SAMPLED_DATA)}'
            ))
