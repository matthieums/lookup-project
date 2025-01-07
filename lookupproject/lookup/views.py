from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse, Http404
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
    print('view called')
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
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
def getTeacher(request):
    teachers = Teacher.objects.all()
    if not teachers.exists():
        raise Http404("No teachers found.")

    if request.method == 'GET':
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCourse(request):
    discipline = request.GET.get('discipline')
    age_group = request.GET.get('age_group')
    radius = request.GET.get('radius')
    user_lon = request.GET.get('user_lon')
    user_lat = request.GET.get('user_lat')

    if not any([discipline, age_group, radius]):
        return Response([])

    courses = Course.objects.all()

    if discipline:
        courses = courses.filter(discipline=discipline)
    if age_group:
        courses = courses.filter(target_audience=age_group)
    if radius:
        user_location = Point(float(user_lon), float(user_lat), srid=4326)
        nearby_schools = School.objects.annotate(
            distance=Distance('coordinates', user_location)
        ).filter(distance__lte=radius * 1000).order_by('distance')

        courses = courses.filter(place__in=nearby_schools)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSchool(request):
    schools = School.objects.all()
    if not schools.exists():
        raise Http404("No school found")

    if request.method == 'GET':
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)


from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .serializers import SchoolSerializer

# Later down the road, consider using django signals
# To get and validate geographic coordinates
@api_view(['POST'])
def get_nearby_locations(request):
    try:
        user_lat = float(request.data.get('user_lat'))
        user_lon = float(request.data.get('user_lon'))
        radius = float(request.data.get('radius'))

        user_location = Point(user_lon, user_lat, srid=4326)

        schools = School.objects.annotate(
            distance=Distance('coordinates', user_location)
        ).filter(distance__lte=radius * 1000).order_by('distance')

        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

    except (TypeError, ValueError):
        if not user_lat or not user_lon or not radius:
            return Response({"error": "Missing required fields."}, status=400)
        else:
            return Response({"error": "Unknown error"},
                            status=400)
