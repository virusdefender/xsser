#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=20, blank=True)
    cookie = models.TextField(blank=True)
    referer = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=300, blank=True)
    top_location = models.CharField(max_length=300, blank=True)
    domain = models.CharField(max_length=50, blank=True)
    screen = models.CharField(max_length=30, blank=True)
    flash = models.CharField(max_length=30, blank=True)
    user_agent = models.CharField(max_length=150, blank=True)
    ip = models.IPAddressField(blank=True)
    title = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return "%s" % (self.create_time, )


class XssProject(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    records = models.ManyToManyField(Record, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    keep_session = models.BooleanField(default=False)
    custom_js = models.BooleanField(default=False)
    custom_js_content = models.TextField(blank=True)

    def __unicode__(self):
        return "%s" % self.title
