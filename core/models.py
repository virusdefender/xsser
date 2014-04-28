#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    cookie = models.TextField(blank=True)
    user_agent = models.CharField(max_length=50, blank=True)
    ip = models.IPAddressField(blank=True)
    url = models.URLField(blank=True)
    title = models.CharField(max_length=50, blank=True)
    keep_session = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.create_time, self.url)


class XssProject(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    records = models.ManyToManyField(Record, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    #js_url = models.URLField()

    def __unicode__(self):
        return "%s" % self.title
