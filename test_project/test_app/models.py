from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from .models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), max_length=64, help_text='Enter a valid email address',required=True,validators=[validators.EmailValidator(message="Invalid Email")])
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta():
        model = User
        fields = ["username","email", "password1", "password2"]


class LoginForm(forms.Form):
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control'}))



class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Company(models.Model):
    name = models.CharField(max_length=255, default='')  # Company name
    domain = models.CharField(max_length=255, default='')  # Company website or domain
    year_founded = models.CharField(max_length=255, default='', null=True, blank=True)  # Year company was founded
    industry = models.CharField(max_length=255, default='')  # Industry type
    size_range = models.CharField(max_length=255, default='', null=True, blank=True)  # Size range of the company (e.g., 50-200 employees)
    locality = models.CharField(max_length=255, default='', null=True, blank=True)  # City or locality
    country = models.CharField(max_length=255, default='')  # Country
    linkedin_url = models.URLField(default='', null=True, blank=True)  # LinkedIn URL
    current_employee_estimate = models.IntegerField(null=True, blank=True)  # Current employee estimate
    total_employee_estimate = models.IntegerField(null=True, blank=True)  # Total employee estimate

    def __str__(self):
        return f"{self.name} - {self.industry}"