#coding=utf-8
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import XssProject, Record


#@login_required(login_url="/login/")
def create_project(request):
    if request.method == "GET":
        return render(request, "core/create_project.html")
    else:
        title = request.POST.get("title")
        if not title:
            return render(request, "info.html", {"info": "请填写标题"})
        p = XssProject.objects.create(user=request.user, title=title)
        return render(request, "core/project/index.html", {"project": p})
