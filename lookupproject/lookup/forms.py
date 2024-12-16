from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'place',
                  'teachers', 'schedule', 'target_audience',
                  'discipline', 'online']
