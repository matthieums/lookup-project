from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.core.mail import send_mass_mail
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponseRedirect
)

from .models import Course, School, CustomUser, STUDENT, TEACHER
from .forms import CourseForm, SchoolForm, NewUserForm, CustomLoginForm
from .serializers import (
    UserSerializer,
    CourseSerializer,
    SchoolSerializer,
    CourseQueryParamsSerializer
)


def index(request):
    return render(request, "lookup/index.html")


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    course_creator = course.created_by

    if request.method == 'GET':
        return render(request, 'lookup/course.html', {
            'course': course,
            'user': user
        })

    elif request.method == 'POST':
        try:
            if user in course.students.all():
                return JsonResponse({'error': 'User is already enrolled in this course.'}, status=400)
            elif course.is_full():
                return JsonResponse({'error': 'Course is full.'}, status=400)

            course.students.add(user)
            # Should I add more logic? Reserializing data and checking that it is 
            # valid before sending it to the db?
            message1 = (
                "A student has enrolled to your course",
                f"{user} enrolled in your course {course.name}",
                "from@example.com",  # What sender email be?
                [course_creator.email]
                )
            message2 = (
                "Succesfully enrolled",
                f"""
                Thank you for enrolling in this course.
                Here is the practical information:
                {course.name}, {course.place}, {course.schedule}
                """,
                "from@example.com",
                [user.email]
            )
            send_mass_mail((message1, message2), fail_silently=False)
            messages.success(
                request,
                f"You\'ve successfully registered to this course. A confirmation"
                f"has been sent to {user.email}"
                )

            return HttpResponseRedirect(reverse('index'))

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Course not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def teachers(request):
    if request.method == 'GET':
        teachers = CustomUser.objects.filter(role=TEACHER).order_by('last_name')

        return render(request, "lookup/teachers.html", {
            'teachers': teachers
        })


def schools(request):
    if request.method == 'GET':
        schools = School.objects.all().order_by('name')
        return render(request, "lookup/schools.html", {
            'schools': schools
        })


def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(CustomUser, pk=teacher_id)
    courses = Course.objects.filter(created_by=teacher_id)
    return render(request, "lookup/teacher_profile.html", {
        'teacher': teacher,
        'courses': courses
    })


def school_profile(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    courses = Course.objects.filter(place=school_id)
    return render(request, "lookup/school_profile.html", {
        'school': school,
        'courses': courses
    })


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect(reverse('login'))
    else:
        form = NewUserForm()

    return render(request, 'lookup/register.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You were successfully logged in!")
                next_url = request.GET.get('next', reverse('index'))
                return HttpResponseRedirect(next_url)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'lookup/login.html', {'form': form})


@login_required
def my_courses(request):
    return render(request, 'lookup/mycourses.html', {
        'user': request.user
    })


@login_required
def new_course(request):
    user = request.user
    if user.role != TEACHER:
        return HttpResponseForbidden(
            "Creating a course is restricted to teachers."
            )

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.instance.created_by = user
            form.save()
            messages.success(request, "Course successfully added!")
            return redirect(reverse(("index")))

    form = CourseForm()

    return render(request, "lookup/new_course.html", {
        'form': form
    })


@login_required
def new_school(request):

    if request.method == 'POST':

        # Customized conversion to point because nothing else
        # seemed to work
        form_data = request.POST.copy()
        raw_value = form_data.get('coordinates') 
        lon, lat = map(float, raw_value.split(','))
        point = Point(lon, lat)
        form_data['coordinates'] = point
        form = SchoolForm(form_data)

        if form.is_valid():
            form.save()
            messages.success(request, "School successfully added")
            return redirect(reverse(('my_courses')))
    else:
        form = SchoolForm()

    return render(request, "lookup/new_school.html", {
        'form': form
    })


def about(request):
    return render(request, "lookup/about.html")


def delete_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        course_creator = course.created_by
        students = course.students

        if course_creator != user:
            return HttpResponseForbidden('Only course creator can delete the course')

        mails = []
        course_name = course.name
        course_place = course.place
        course_schedule = course.schedule
        for student in students.all():
            mail = (
                "Course cancellation",
                f"""
                This message was sent because a course you were enrolled
                in was deleted. We are sorry:
                {course_name}, {course_place}, {course_schedule}
                """,
                "from@example.com",
                [student.email]
            )
            mails.append(mail)
        course.delete()
        send_mass_mail((mail for mail in mails), fail_silently=False)
        messages.success(
            request,
            """Course successfully deleted. A message has
            been sent to all participants"""
        )

    return HttpResponseRedirect(reverse('index'))


@login_required
def participants(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    course_creator = course.created_by

    if user.id != course_creator.id:
        return HttpResponseForbidden(
            'Only the creator of this course can access its participants list.'
        )

    return render(request, 'lookup/participants.html', {
            'course': course
        })


############ API'S ############
@api_view(['GET'])
def getTeacher(request):
    teachers = CustomUser.objects.filter(role=TEACHER)
    if not teachers.exists():
        raise Http404("No teachers found.")

    if request.method == 'GET':
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCourse(request):
    serializer = CourseQueryParamsSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    user_id = request.GET.get('id')
    discipline = request.GET.get('discipline')
    age_group = request.GET.get('age_group')
    radius = request.GET.get('radius')
    user_lon = request.GET.get('user_lon')
    user_lat = request.GET.get('user_lat')

    if not any([discipline, age_group, radius, user_id]):
        return HttpResponseBadRequest('Empty query parameters')

    courses = Course.objects.all()

    if user_id:
        user = CustomUser.objects.get(id=user_id)
        if user.is_student():
            courses = courses.filter(students=user)
        elif user.is_teacher():
            courses = courses.filter(created_by=user_id)
    if discipline:
        courses = courses.filter(discipline=discipline)
    if age_group:
        courses = courses.filter(target_audience=age_group)
    if radius:
        try:
            user_lon = float(user_lon)
            user_lat = float(user_lat)
            user_location = Point(float(user_lon), float(user_lat), srid=4326)
            nearby_schools = School.objects.filter(
                coordinates__distance_lte=(user_location, D(km=radius))
            )
            courses = courses.filter(place__in=nearby_schools)
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Invalid latitude or longitude values')

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
