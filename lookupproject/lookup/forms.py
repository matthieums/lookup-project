from django import forms
from .models import Course, School


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'place',
                  'teachers', 'schedule', 'target_audience',
                  'discipline', 'online']

class SchoolForm(forms.ModelForm):
    
    class Meta:
        model = School
        fields = ['name', 'location', 'contact', 'website']