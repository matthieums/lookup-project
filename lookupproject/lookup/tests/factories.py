from faker import Faker
from faker.providers import BaseProvider, DynamicProvider
import factory
from lookup.models import Course, Teacher, School
from lookup.models import DISCIPLINE_CHOICES, TARGET_AUDIENCE_CHOICES
import random
from django.utils import timezone


fake = Faker()

styles = {
    'dance': ['Salsa', 'Tango', 'Bachata', 'Jive', 'Rock'],
    'drama': ['Improv', 'Declamation', 'Eloquence'],
    'music': ['Piano', 'violin', 'Singing', 'Cello']
}

random_style_provider = DynamicProvider(
    provider_name='style',
    elements=[random.choice(random.choice(list(styles.values())))],
)


class Audiences(BaseProvider):
    def randomAudience(self) -> str:
        return random.choice(list(TARGET_AUDIENCE_CHOICES.values()))


class Disciplines(BaseProvider):
    def randomDiscipline(self):
        return random.choice(list(DISCIPLINE_CHOICES.values()))


fake.add_provider(random_style_provider)
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

    name = fake.style()
    print(f'generated name:{name}')
    description = factory.Faker('text')
    schedule = timezone.make_aware(fake.date_time_this_year())
    target_audience = fake.randomAudience()
    discipline = fake.randomDiscipline()
    online = False
