from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models as gis_models

from lookup.validators import validate_location


# Multiple choices for the discipline
MUSIC = 'music'
DANCE = 'dance'
DRAMA = 'drama'
DISCIPLINE_CHOICES = {
    MUSIC: 'music',
    DANCE: 'dance',
    DRAMA: 'drama'
}

# Multiple choices for target audiences
ANYONE = 'anyone'
ELDERLY = 'elderly'
ADULTS = 'adults'
ADOLESCENTS = 'adolescents'
CHILDREN = 'children'
TARGET_AUDIENCE_CHOICES = {
    ANYONE: 'Anyone',
    ELDERLY: 'Elderly',
    ADULTS: 'Adults',
    ADOLESCENTS: 'Adolescents',
    CHILDREN: 'Children'
}

# User roles
STUDENT = 'student'
TEACHER = 'teacher'


class CustomUser(AbstractUser):

    class Meta:
        db_table = 'lookup_customuser'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
        )

    def is_student(self):
        return self.role == STUDENT

    def is_teacher(self):
        return self.role == TEACHER


class School(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, validators=[validate_location])
    coordinates = gis_models.PointField(blank=True, null=True, srid=4326)
    contact = models.EmailField(max_length=254, unique=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=800)
    illustration = models.ImageField(
        blank=True,
        upload_to='images/',
        default='default/default_image.jpg')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='course_creator',
        default='23'
        )
    place = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        verbose_name='where the course takes place'
        )
    teachers = models.ManyToManyField(CustomUser, related_name='courses')
    schedule = models.DateTimeField(
        auto_now=False,
        auto_now_add=False
        )
    target_audience = models.CharField(
        choices=TARGET_AUDIENCE_CHOICES,
        default=ANYONE,
        max_length=20
    )
    discipline = models.CharField(choices=DISCIPLINE_CHOICES)
    online = models.BooleanField(default=False)
    students = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='enrolled_courses',
        verbose_name='students enrolled in this course'
        )
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.name}, created by {self.created_by}'

    def is_full(self):
        return self.students.count() >= self.capacity
