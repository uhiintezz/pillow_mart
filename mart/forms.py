from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from .models import *


class RegisterUserForm(UserCreationForm):

    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'type':"text",  'class': "form-control", 'id':"name",  'name':"name",  'value':"", 'placeholder':"Username"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'type':"email", 'class':"form-control", 'id':"password", 'name':"email", 'value':"", 'placeholder':"Email"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'type':"password", 'class':"form-control", 'id':"password", 'name':"password1", 'value':"",'placeholder':"Password"}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'type':"password", 'class':"form-control", 'id':"password", 'name':"password2", 'value':"", 'placeholder':"Confirm Password"}))
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'type':"checkbox", 'id':"f-option", 'name':"selector"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'type':"text",  'class': "form-control", 'id':"name",  'name':"name",  'value':"", 'placeholder':"Username"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'type': "password", 'class': "form-control", 'id': "password", 'name': "password1", 'value': "",
               'placeholder': "Password"}))
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'type':"checkbox", 'id':"f-option", 'name':"selector"}))

