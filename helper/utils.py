# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import hashlib
import json

from django.core.mail import send_mail
from django.http import HttpResponse

from liyan.settings import EMAIL_HOST_USER
from liyan.settings import DEBUG
from liyan.settings import site_name


def json_response(flag=False, code='', msg='', content=''):
    return HttpResponse(json.dumps({'flag': flag, 'code': code, 'msg': msg, 'data': content}))


def send_email(Subject, message, to):
    send_mail(Subject, message, EMAIL_HOST_USER,
              [to], fail_silently=False)


def generate_register_code(user_id=None):
    return hashlib.md5(str(user_id)).hexdigest().upper()


def custom_processors(request):
    return {
        'site_name': site_name,
        'DEBUG': DEBUG,
    }
