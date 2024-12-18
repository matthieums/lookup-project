from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("courses", views.courses, name="courses"),
    path("teachers", views.teachers, name="teachers"),
    path("schools", views.schools, name="schools"),
    path("contact", views.contact, name="contact"),
    path("newschool", views.new_school, name="new_school"),


    # API endpoints
    path("teachers/<int:teacher_id>", views.getTeacher, name="getTeacher"),
    path("courses/<int:course_id>", views.getCourse, name="getCourse"),
    path("schools/<int:school_id>", views.getSchool, name="getSchool")
]
