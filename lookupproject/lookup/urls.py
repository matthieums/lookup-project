from django.urls import path, include
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", views.register, name="register"),

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
    path("enroll/<int:course_id>", views.enroll, name="enroll"),

    # API endpoints
    path("teachers/get", views.getTeacher, name="getTeacher"),
    path("courses/get/", views.getCourse, name="getCourse"),
    path("schools/get/", views.getSchool, name="getSchool"),
    path("geoschool", views.get_nearby_locations, name="geoschool"),

]
