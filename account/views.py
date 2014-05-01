#coding=utf-8
import json
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render, redirect
from .forms import RegisterForm

def message(status, content):
    response_json = {"status": status, "content": content}
    return HttpResponse(json.dumps(response_json))

"""
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", " ").strip()
        email = request.POST.get("email", " ").strip()
        password = request.POST.get("password", " ").strip()
        password1 = request.POST.get('password1', " ").strip()

        if not (3 <= len(username) <= 10):
            return message("error", u"Invalid username length")

        r = re.compile(r"[A-Za-z0-9\u4e00-\u9fa5]+")
        if not r.match(username):
            return message("error", u"Invalid username format")

        username_is_exist = User.objects.filter(username=username).exists()
        if username_is_exist:
            return message("error", u"Username already exists")

        r = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not r.match(email):
            return message("error", u"Invalid email format")

        email_is_exist = User.objects.filter(email=email).exists()
        if email_is_exist:
            return message("error", u"Email already exists")

        if password != password1:
            return message("error", u"Two passwords do not match")

        if len(password) < 6:
            return message("error", u"Password is too short")

        User.objects.create_user(username=username, password=password, email=email)
        next = request.POST.get("next", "/my_projects/")
        response_json = {"status": "success", "redirect": next}
        return HttpResponse(json.dumps(response_json))

    else:
        next = request.GET.get("next", "/my_projects/")
        return render(request, "account/register_form.html", {"next": next})

"""


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            email = register_form.cleaned_data["email"]
            password = register_form.cleaned_data["password"]
            User.objects.create_user(username=username, password=password, email=email)
            next = request.POST.get("next", "/my_projects/")
            response_json = {"status": "success", "redirect": next}
            return HttpResponse(json.dumps(response_json))
        else:
            #print repr(register_form.errors)
            response_json = {"status": "error", "content": register_form.errors.items()[0][1][0]}
            return HttpResponse(json.dumps(response_json))
    else:
        next = request.GET.get("next", "/my_projects/")
        return render(request, "account/register_form.html", {"next": next})



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.logout(request)
            auth.login(request, user)
            next = request.POST.get("next", "/my_projects/")
            #if next == "" or "/register/":
            #next = "/"
            response_json = {"status": "success", "redirect": next}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": u"Invalid Username or password"}
            return HttpResponse(json.dumps(response_json))
    else:
        next = request.GET.get("next", "/my_projects/")
        return render(request, "account/login_form.html", {"next": next})


def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required(login_url="/login/")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if len(password1) < 6:
                return message("error", "Password is too short")
            if auth.authenticate(username=request.user.username, password=old_password):
                user = User.objects.get(username=request.user.username)
                user.set_password(password1)
                user.save()
                auth.logout(request)
                response_json = {"status": "success", "redirect": "/login/"}
                return HttpResponse(json.dumps(response_json))
            else:
                response_json = {"status": "error", "content": u"Old password is incorrect"}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content": u"Two passwords do not match"}
            return HttpResponse(json.dumps(response_json))
    else:
        return render(request, "account/change_password.html")
