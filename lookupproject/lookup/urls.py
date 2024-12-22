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
    path("teachers/<int:teacher_id>",
         views.teacher_profile,
         name="teacher_profile"
         ),
    path("schools/<int:school_id>",
         views.school_profile,
         name="school_profile"
         ),
    path("success", views.success, name="success"),


    # API endpoints
    path("teachers/get/<int:teacher_id>", views.getTeacher, name="getTeacher"),
    path("courses/get/<str:course_discipline>", views.getCourse, name="getCourse"),
    path("schools/get/<int:school_id>", views.getSchool, name="getSchool")
]
