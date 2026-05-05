from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


GRADE_CHOICES = [
    ('', '-- Grade --'),
    ('A', 'A (5)'),
    ('B', 'B (4)'),
    ('C', 'C (3)'),
    ('D', 'D (2)'),
    ('E', 'E (1)'),
    ('F', 'F (0)'),
]

GRADE_POINTS = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}


class SemesterForm(forms.Form):
    semester = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. 100L First Semester'
        })
    )