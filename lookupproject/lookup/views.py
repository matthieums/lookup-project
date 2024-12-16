from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from lookup.models import Course, Teacher, School
import json
from .serializers import TeacherSerializer, CourseSerializer, SchoolSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

def index(request):
    return render(request, "lookup/index.html")


def courses(request):
    return render(request, "lookup/courses.html")


def teachers(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()

        return render(request, "lookup/teachers.html", {
            'teachers': teachers
        })


def schools(request):
    return render(request, "lookup/schools.html")


def contact(request):
    return render(request, "lookup/contact.html")


def about(request):
    return render(request, "lookup/about.html")


@api_view(['GET'])
def getTeacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        return JsonResponse({
            "error": f"Teacher with id {teacher_id} does not exist"
        })

    if request.method == 'GET':
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)


@api_view(['GET'])
def getCourse(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return JsonResponse({
            "error": f"Course with id {course_id} does not exist"
        })

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)


@api_view(['GET'])
def getSchool(request, school_id):
    try:
        school = School.objects.get(pk=school_id)
    except School.DoesNotExist:
        return JsonResponse({
            "error": f"School with id {school_id} does not exist"
        })

    if request.method == 'GET':
        serializer = SchoolSerializer(school)
        return Response(serializer.data)