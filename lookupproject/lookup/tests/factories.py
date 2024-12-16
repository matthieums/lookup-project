from faker import Faker
import factory
from lookup.models import Course, Teacher, School
from faker.providers import BaseProvider
import random

fake = Faker()


class danceStyle(BaseProvider):
    def style(self) -> str:
        return random.choice(['Salsa', 'Tango', 'Bachata', 'Jive', 'Rock'])


fake.add_provider(danceStyle)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School
    name = factory.Faker('company')
    location = factory.Faker('address')
    contact = factory.Faker('email')
    website = factory.Faker('url')


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher
    name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    disciplines = 'Music'
    mailaddress = factory.Faker('email')
    phone_number = '+55 555 55'


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    name = fake.style()
    description = factory.Faker('text')
    schedule = factory.Faker('date_time')
    target_audience = 'anyone'
    discipline = 'dance'
    online = False
