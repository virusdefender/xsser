from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xsser.views.home', name='home'),
    # url(r'^xsser/', include('xsser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.my_projects', name="index"),
    url(r'^create_project/$', 'core.views.create_project', name="create_project"),
    url(r'^project/$', 'core.views.project_detail', name="project_detail"),
    url(r'^project/delete', 'core.views.delete_project', name="delete_project"),
    url(r'^xss/$', 'core.views.xss_js', name="xss_js"),
    url(r'^get_cookie/$', 'core.views.get_cookie', name="get_cookie"),
    url(r'^my_projects/$', 'core.views.my_projects', name="my_projects"),
    url(r'^project/settings/(?P<project_id>\d+)/$', 'core.views.project_settings', name="project_settings"),
    url(r'^project/test/', 'core.views.func_test', name="func_test"),

    url('^login/$', 'account.views.login', name="login"),
    url(r'^register/$', 'account.views.register', name="register"),
    url(r'^change_password/$', 'account.views.change_password', name="change_password"),
    url(r'^logout/$', 'account.views.logout', name="logout"),

)
