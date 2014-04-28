from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    cookie = models.TextField(blank=True)
    user_agent = models.CharField(max_length=50, blank=True)
    ip = models.IPAddressField(blank=True)
    url = models.URLField(balnk=True)
    title = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.create_time, self.url)


class XssProject(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    records = models.ManyToManyField(Record, balnk=True, null=True)
    create_time = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.title
