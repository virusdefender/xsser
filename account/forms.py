#coding=utf-8
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                               error_messages={"required": "Please input username",
                                               "invalid": "Invalid username",
                                               "max_length": "Username is too long"})
    email = forms.EmailField(max_length=30, required=True,
                             error_messages={"required": "Please input email",
                                             "invalid": "Invalid email",
                                             "max_length": "Email is too long"})
    password = forms.CharField(min_length=6, max_length=20, required=True,
                               error_messages={"required": "Please input password",
                                               "min_length": "Password is too short",
                                               "max_length": "Password is too long"})
    password1 = forms.CharField(min_length=6, max_length=20, required=True,
                                error_messages={"required": "Please confirm password",
                                                "min_length": "Password is too short",
                                                "max_length": "Password is too long"})

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data["username"])
            raise forms.ValidationError("Username already exist")
        except User.DoesNotExist:
            return self.cleaned_data["username"]

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data["email"])
            raise forms.ValidationError("Email already exist")
        except User.DoesNotExist:
            return self.cleaned_data["email"]

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["password1"]:
            raise forms.ValidationError("Two passwords do not match")
        else:
            return self.cleaned_data["password"]


