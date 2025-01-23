from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("", views.index, name="index"),
     path("about", views.about, name="about"),
     path("courses", views.courses, name="courses"),
     path("teachers", views.teachers, name="teachers"),
     path("schools", views.schools, name="schools"),
     path("contact", views.contact, name="contact"),
     path("newschool", views.new_school, name="new_school"),
     path("mycourses", views.my_courses, name="my_courses"),

     path("teachers/<int:teacher_id>",
          views.teacher_profile,
          name="teacher_profile"
          ),
     path("schools/<int:school_id>",
          views.school_profile,
          name="school_profile"
          ),

     path("success", views.success, name="success"),
     path("course/<int:course_id>", views.course, name="course"),
     path(
          "enroll/<int:course_id>/participants",
          views.participants,
          name="participants"
          ),

     # Authentication logic
     path("accounts/", include("django.contrib.auth.urls")),
     path("accounts/register", views.register, name="register"),
     path("accounts/login/", auth_views.LoginView.as_view()),

     # API endpoints
     path("teachers/get", views.getTeacher, name="getTeacher"),
     path("courses/get/", views.getCourse, name="getCourse"),
     path("schools/get/", views.getSchool, name="getSchool"),
     path("geoschool", views.get_nearby_locations, name="geoschool"),
     path("delete/<int:course_id>", views.delete_course, name="delete_course")
]
