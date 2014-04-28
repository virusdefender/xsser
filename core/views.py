#coding=utf-8
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from xsser.settings import BASE_URL
from .models import XssProject, Record


@login_required(login_url="/login/")
def create_project(request):
    if request.method == "GET":
        return render(request, "core/create_project.html")
    else:
        title = request.POST.get("title")
        if not title:
            return render(request, "info.html", {"info": "请填写标题"})
        if len(title) > 25:
            title = title[:25]
        p = XssProject.objects.create(user=request.user, title=title)
        return render(request, "core/project_index.html", {"project": p})


def project_index(request):
    project_id = request.GET.get("id", "-1")
    try:
        p = XssProject.objects.get(id=int(project_id))
    except XssProject.DoesNotExist:
        raise Http404
    return render(request, "core/project_index.html", {"project": p, "base_url": BASE_URL})
