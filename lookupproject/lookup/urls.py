from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("", views.index, name="index"),
     path("about", views.about, name="about"),
     path("teachers", views.teachers, name="teachers"),
     path("schools", views.schools, name="schools"),
     path("new_course", views.new_course, name="new_course"),
     path("new_school", views.new_school, name="new_school"),
     path("mycourses", views.my_courses, name="my_courses"),

     # Api dependant paths
     path("course/<int:course_id>", views.course, name="course"),
     path("course/<int:course_id>/participants",
          views.participants,
          name="participants"
          ),
     path("teachers/<int:teacher_id>",
          views.teacher_profile,
          name="teacher_profile"
          ),
     path("schools/<int:school_id>",
          views.school_profile,
          name="school_profile"
          ),
     path("delete/<int:course_id>", views.delete_course, name="delete_course"),

     # Authentication logic
     path("accounts/register", views.register, name="register"),
     path("accounts/login/", views.login_view, name="login"),
     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

     # API endpoints
     path("teachers/get", views.getTeacher, name="getTeacher"),
     path("courses/get/", views.getCourse, name="getCourse"),
     path("schools/get/", views.getSchool, name="getSchool"),
]
