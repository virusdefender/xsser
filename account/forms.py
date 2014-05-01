#coding=utf-8
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                               error_messages={"required": "Please input username",
                                               "invalid": "Invalid username",
                                               "max_length": "Username is too long"})
    password = forms.CharField(required=True,
                               error_messages={"required": "Please input password"})


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
    confirm_password = forms.CharField(min_length=6, max_length=20, required=True,
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
        super(RegisterForm, self).clean()
        if "password" in self.cleaned_data and "confirm_password" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
                raise forms.ValidationError("Two passwords do not match")
        return self.cleaned_data


class ChangePswForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                               error_messages={"required": "Please input username",
                                               "invalid": "Invalid username",
                                               "max_length": "Username is too long"})
    old_password = forms.CharField(required=True,
                                   error_messages={"required": "Please input old password"})
    new_password = forms.CharField(min_length=6, max_length=20, required=True,
                                   error_messages={"required": "Please input password",
                                                   "min_length": "New password is too short",
                                                   "max_length": "New Password is too long"})
    confirm_new_password = forms.CharField(min_length=6, max_length=20, required=True,
                                           error_messages={"required": "Please confirm password",
                                                           "min_length": "New Password is too short",
                                                           "max_length": "New password is too long"})

    def clean(self):
        super(ChangePswForm, self).clean()
        if "new_password" in self.cleaned_data and "confirm_new_password" in self.cleaned_data:
            if self.cleaned_data["new_password"] != self.cleaned_data["confirm_new_password"]:
                raise forms.ValidationError("Two passwords do not match")
        return self.cleaned_data

