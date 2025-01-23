# TO-DO : Add validators for emails, urls, etc.
# TO-DO : Add the possibility to add a picture => Will need the Pillow
# library and an imageField.
# TO-DO: import library to check phone numbers
# If a class is online, what do I do with addresses etc?
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


    # def save(self, *args, **kwargs):
    #     # is_new = self.pk is None
    #     super().save(*args, **kwargs)

        # if is_new:
        #     if self.role == STUDENT:
        #         StudentProfile.objects.create(user=self)
        #     elif self.role == TEACHER:
        #         TeacherProfile.objects.create(user=self)



# User's default fields:
# id
# username
# first_name
# last_name
# email
# password
# ...

# class StudentProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')


class School(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, validators=[validate_location])
    coordinates = models.PointField(blank=True, null=True, srid=4326)
    contact = models.EmailField(max_length=254, unique=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=800)
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

    
# class TeacherProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')

#     schools = models.ManyToManyField(
#         School,
#         related_name='teachers',
#         verbose_name='school where this person teaches',
#         blank=True
#         )
#     discipline = models.CharField(choices=DISCIPLINE_CHOICES, max_length=20)
#     phone_number = models.CharField(max_length=15, blank=True)

#     def serialize(self):
#         return serializers.serialize('json', [self])
    
#     def __str__(self) -> str:
#         return f"{self.user.first_name} {self.user.last_name}"



