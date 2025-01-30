from django import forms
from .models import Course, School, CustomUser, TEACHER, STUDENT
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[(STUDENT, 'Student'), (TEACHER, 'Teacher')])
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = 'required'

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
                  'discipline', 'online', 'created_by', 'illustration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['created_by'].widget = forms.HiddenInput()

        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'
            if field_name != 'online':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


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
            field.widget.attrs['class'] = 'form-control'
