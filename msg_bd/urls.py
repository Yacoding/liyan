# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from django.conf.urls import patterns, url
from msg_bd import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^new_msg', views.new_msg, name='new_msg'),
                       url(r'^get_msg', views.get_msg, name='get_msg'),
                       url(r'^reply_msg', views.reply_msg, name='reply'),
                       url(r'^delete_msg', views.delete_msg, name='delete_msg'),

)