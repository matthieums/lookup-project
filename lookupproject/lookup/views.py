from django.shortcuts import render

def index(request):
    return render(request, "lookup/index.html")

def classes(request):
    return render(request, "lookup/classes.html")

def teachers(request):
    return render(request, "lookup/teachers.html")

def schools(request):
    return render(request, "lookup/schools.html")

def contact(request):
    return render(request, "lookup/contact.html")

def about(request):
    return render(request, "lookup/about.html")

