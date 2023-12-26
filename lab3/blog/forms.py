from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Blog


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(help_text="", label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(help_text="", label="Подтвердите пароль", widget=forms.PasswordInput)
    username = forms.CharField(help_text="", label="Логин")
    email = forms.CharField(help_text="", label="Электронная почта")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class CreateBlogPost(forms.ModelForm):
    name = forms.CharField(help_text="", label="Имя")
    description = forms.CharField(help_text="", label="Описание")

    class Meta:
        model = Blog
        fields = ['name', 'description']

