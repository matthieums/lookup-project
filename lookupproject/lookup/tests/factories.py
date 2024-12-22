from faker import Faker
from faker.providers import BaseProvider
import factory
from lookup.models import Course, Teacher, School
from lookup.models import DISCIPLINE_CHOICES, TARGET_AUDIENCE_CHOICES
import random


fake = Faker()


class Styles(BaseProvider):
    def randomStyle(self) -> str:
        styles = {
            'dance': ['Salsa', 'Tango', 'Bachata', 'Jive', 'Rock'],
            'drama': ['Improv', 'Declamation', 'Eloquence'],
            'music': ['Piano', 'violin', 'Singing', 'Cello']
        }
        random_list = random.choice(list(styles.values()))
        return random.choices(random_list)


class Audiences(BaseProvider):
    def randomAudience(self) -> str:
        return random.choice(list(TARGET_AUDIENCE_CHOICES.values()))


class Disciplines(BaseProvider):
    def randomDiscipline(self):
        return random.choice(list(DISCIPLINE_CHOICES.values()))


fake.add_provider(Styles)
fake.add_provider(Audiences)
fake.add_provider(Disciplines)


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
    disciplines = fake.randomDiscipline()
    mailaddress = factory.Faker('email')
    phone_number = '+55 555 55'


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
    name = fake.randomStyle()
    description = factory.Faker('text')
    schedule = factory.Faker('date_time')
    target_audience = fake.randomAudience()
    discipline = random.choice(['music', 'dance', 'drama'])
    online = False
