from faker import Faker
from faker.providers import BaseProvider, DynamicProvider
import factory
from lookup.models import Course, School, CustomUser
from lookup.models import DISCIPLINE_CHOICES, TARGET_AUDIENCE_CHOICES
import random
from django.utils import timezone
from django.contrib.gis.geos import Point

STYLES = {
    'dance': ['Salsa', 'Tango', 'Bachata', 'Jive', 'Rock'],
    'drama': ['Improv', 'Declamation', 'Eloquence'],
    'music': ['Piano', 'violin', 'Singing', 'Cello']
}

fake = Faker()

class Audiences(BaseProvider):
    def randomAudience(self) -> str:
        return random.choice(list(TARGET_AUDIENCE_CHOICES.values()))


class Disciplines(BaseProvider):
    def randomDiscipline(self):
        return random.choice(list(DISCIPLINE_CHOICES.values()))


random_style_provider = DynamicProvider(
    provider_name='style',
    elements=[random.choice(random.choice(list(STYLES.values())))],
)

fake.add_provider(random_style_provider)
fake.add_provider(Audiences)
fake.add_provider(Disciplines)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.LazyAttribute(lambda _: fake.company())
    location = factory.LazyAttribute(lambda _: fake.city())
    coordinates = factory.LazyAttribute(lambda _: Point(float(fake.longitude()), float(fake.latitude())))
    contact = factory.LazyAttribute(lambda _: fake.email())
    website = factory.LazyAttribute(lambda _: fake.url())


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    role = 'teacher'

class StudentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    role = 'student'


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = fake.style()
    description = factory.Faker('text')
    schedule = timezone.make_aware(fake.date_time_this_year())
    target_audience = factory.LazyAttribute(lambda _: fake.randomAudience())  # LazyAttribute needed for dynamic audience selection
    discipline = factory.LazyAttribute(lambda _: fake.randomDiscipline())
    online = False
