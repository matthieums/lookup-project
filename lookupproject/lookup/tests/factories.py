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
    def randomAudience(self):
        return random.choice(list(TARGET_AUDIENCE_CHOICES.values()))


class Styles(BaseProvider):
    def randomStyle(self, category=None):
        if category and category in STYLES:
            return random.choice(STYLES[category])
        all_disciplines = [disc for sublist in STYLES.values() for disc in sublist]
        return random.choice(all_disciplines)


class Coordinates(BaseProvider):
    coordinates = [
        (50.8503, 4.3517),
        (51.2194, 4.4025),
        (50.6400, 5.5700),
        (50.9333, 3.1000),
        (51.0000, 4.5000),
        (51.1800, 4.4000),
        (50.8594, 4.6997),
        (51.2154, 3.2252),
        (50.7579, 3.2895),
        (51.2200, 4.4036),
    ]  

    def randomCoordinates(self):
        lat, lon = random.choice(self.coordinates)
        return Point(lon, lat)

fake.add_provider(Styles)
fake.add_provider(Audiences)
fake.add_provider(Coordinates)


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.LazyAttribute(lambda _: fake.company())
    location = factory.LazyAttribute(lambda _: fake.city())
    coordinates = factory.LazyAttribute(lambda _: fake.randomCoordinates())
    contact = factory.LazyAttribute(lambda _: fake.email())
    website = factory.LazyAttribute(lambda _: fake.url())


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    first_name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')


class TeacherFactory(CustomUserFactory):
    role = 'teacher'


class StudentFactory(CustomUserFactory):
    role = 'student'


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    description = factory.Faker('text')
    schedule = timezone.make_aware(fake.date_time_this_year())
    target_audience = factory.LazyAttribute(lambda _: fake.randomAudience())  # LazyAttribute needed for dynamic audience selection
    online = False
    capacity = fake.pyint(10, 30, 5)


class DanceCourses(CourseFactory):
    name = factory.LazyAttribute(lambda _: fake.randomStyle('dance'))
    discipline = 'dance'


class DramaCourses(CourseFactory):
    name = factory.LazyAttribute(lambda _: fake.randomStyle('drama'))
    discipline = 'drama'


class MusicCourses(CourseFactory):   
    name = factory.LazyAttribute(lambda _: fake.randomStyle('music'))
    discipline = 'music'
