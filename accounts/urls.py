# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^active/(?P<active_code>\w+)/$', views.active, name='active'),
                       url(r'^send_active_email/(?P<user_id>\w+)/$', views.send_active_email, name='re_active'),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^check_detail/$', views.check_detail, name='check_detail'),
                       url(r'^reset_password/$', views.reset_password, name='reset_password'),
)