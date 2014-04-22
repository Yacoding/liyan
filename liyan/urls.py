# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import django_databrowse

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'liyan.views.home', name='home'),
                       # url(r'^liyan/', include('liyan.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/',  include('accounts.urls', namespace="accounts")),
                       url(r'^msg_bd/',  include('msg_bd.urls', namespace="msg_bd")),

                       #  默认首页
                       url(r'^$',  'accounts.views.index'),
                       )
