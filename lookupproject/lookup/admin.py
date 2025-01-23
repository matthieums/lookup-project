from django.contrib import admin
from .models import Course, CustomUser, School

# Register your models here.
admin.site.register(Course)
admin.site.register(CustomUser)
admin.site.register(School)