from django import forms
from .models import Course, School, CustomUser, TEACHER, STUDENT
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):

    role = forms.ChoiceField(choices=[(STUDENT, 'Student'), (TEACHER, 'Teacher')])
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in [TEACHER, STUDENT]:
            raise forms.ValidationError("Invalid role")
        return role


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
        fields = ['name', 'location', 'coordinates',
                  'contact', 'website']
        widgets = {
            'location': forms.HiddenInput,
            'coordinates': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'


class enrollForm(forms.Form):
    first_name = forms.CharField(max_length=52)
    last_name = forms.CharField(max_length=52)
    email = forms.EmailField()