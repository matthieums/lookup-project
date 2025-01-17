# TO-DO : Add validators for emails, urls, etc.
# TO-DO : Add the possibility to add a picture => Will need the Pillow
# library and an imageField.
# TO-DO: import library to check phone numbers
# If a class is online, what do I do with addresses etc?
from django.core import serializers
from django.db import models
from lookup.validators import validate_location
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import Point

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


class customUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
class School(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, validators=[validate_location])
    coordinates = models.PointField(blank=True, null=True)
    contact = models.EmailField(max_length=254, unique=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    schools = models.ManyToManyField(
        School,
        related_name='teachers',
        verbose_name='school where this person teaches'
        )
    disciplines = models.CharField(choices=DISCIPLINE_CHOICES, max_length=20)
    mailaddress = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15)

    def serialize(self):
        return serializers.serialize('json', [self])
    
    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=800)
    place = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='where the course takes place'
        )
    teachers = models.ManyToManyField(Teacher, related_name='courses')
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

    def __str__(self) -> str:
        return self.name
