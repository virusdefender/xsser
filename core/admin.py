#coding=utf-8
from django.contrib import admin
from .models import XssProject, Record

admin.site.register(XssProject)
admin.site.register(Record)