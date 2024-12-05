from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("courses", views.courses, name="courses"),
    path("teachers", views.teachers, name="teachers"),
    path("schools", views.schools, name="schools"),
    path("contact", views.contact, name="contact"),
]