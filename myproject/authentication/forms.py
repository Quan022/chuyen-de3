from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Course, Lesson


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content']



