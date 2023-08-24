from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student


class StudentCreation(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email']


class StudentEdit(UserChangeForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email']
