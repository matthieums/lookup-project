from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from lookup.models import Course, Teacher, School
import json
from .serializers import TeacherSerializer, CourseSerializer, SchoolSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import CourseForm, SchoolForm, enrollForm


def index(request):
    return render(request, "lookup/index.html")


def courses(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, "lookup/courses.html", {
            'courses': courses
        })


def teachers(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()

        return render(request, "lookup/teachers.html", {
            'teachers': teachers
        })


def schools(request):
    if request.method == 'GET':
        schools = School.objects.all()
        return render(request, "lookup/schools.html", {
            'schools': schools
        })


def contact(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("success")
    else:
        form = CourseForm()

    return render(request, "lookup/contact.html", {
        'form': form
    })


def about(request):
    return render(request, "lookup/about.html")


def new_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect
    else:
        form = SchoolForm()
    return render(request, "lookup/newschool.html", {
        'form': form
    })


def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, "lookup/teacher_profile.html", {
        'teacher': teacher
    })


def school_profile(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    return render(request, "lookup/school_profile.html", {
        'school': school
    })


def success(request):
    return render(request, 'lookup/success.html')


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = enrollForm()

    return render(request, 'lookup/course.html', {
        'course': course,
        'form': form
    })

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
def getCourse(request, course_discipline):
    course = Course.objects.filter(discipline=course_discipline.lower())
    if not course.exists():
        return JsonResponse({
            "error": f"Course with id {course_discipline} does not exist"
        })

    if request.method == 'GET':
        serializer = CourseSerializer(course, many=True)
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