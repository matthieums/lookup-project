from django import forms
from .models import Course, School


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'place',
                  'teachers', 'schedule', 'target_audience',
                  'discipline', 'online']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'location', 'contact', 'website']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'