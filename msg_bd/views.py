# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from liyan.settings import DOMAIN
from helper.utils import send_email
from helper.utils import json_response
from models import Msg


def index(request):
    ret = {}
    if request.user.is_authenticated():
        ret['username'] = request.user.username
        return render_to_response("msg_bd/index.html",
                                  ret,
                                  context_instance=RequestContext(request))
    return render_to_response("msg_bd/index.html",
                              ret,
                              context_instance=RequestContext(request))


@csrf_exempt
def new_msg(request):
    if 'content' in request.POST and 'contact_email' in request.POST:
        msg = Msg(content=request.POST.get('content'), contact_email=request.POST.get('contact_email'))
        if request.user.is_authenticated():
            msg.user = request.user
            msg.user_name = request.user.username
        msg.save()
        ret = {
            'content': msg.content,
            'contact_email': msg.contact_email,
            'create_time': msg.create_time.strftime("%Y-%m-%d"),
            'user_name': msg.user_name,
            'msg_id': msg.id,
        }
        return json_response(True, '0', 'success', ret)
    else:
        return json_response(False, '020001', 'lack of parameter')


def get_msg(request):
    msgs = Msg.objects.all()
    ret = []
    for msg in msgs:
        item = {
            'user_name': msg.user_name,
            'contact_email': msg.contact_email,
            'create_time': msg.create_time.strftime("%Y-%m-%d"),
            'content': msg.content,
            'msg_id': msg.id,
        }
        ret.append(item)
    return json_response(True, '0', 'success', ret)


@csrf_exempt
def reply_msg(request):
    if not 'reply_content' in request.POST and not 'reply_user' in request.POST and not 'msg_id' in request.POST and \
            not 'email' in request.POST:
        return json_response(False, '020002', 'lack of parameter')
    try:
        msg = Msg.objects.get(id=request.POST.get("msg_id"))
        reply = Msg(contact_email=request.POST.get("email"), content=request.POST.get('reply_content'), msg_type=1,
                    msg_reply_to=msg)
        msg.has_reply = True
        msg.save()
        if request.user.is_authenticated():
            reply.user = request.user
            reply.user_name = request.user.username
        reply.save()
        ret = {
            'content': reply.content,
            'contact_email': reply.contact_email,
            'create_time': reply.create_time.strftime("%Y-%m-%d"),
            'user_name': reply.user_name,
            'msg_id': reply.id,
            'reply_to_msg': msg.id,
        }
        return json_response(True, '0', 'success', ret)
    except Msg.DoesNotExist:
        return json_response(False, '020003', '留言不存在')
    except Exception, e:
        print e
        return json_response(False, '020004', '数据库错误')


@csrf_exempt
def delete_msg(request):
    # TODO check user type
    if 'msg_id' not in request.POST:
        return json_response(False, '020003', 'lack of parameter')
    try:
        msg = Msg.objects.get(id=request.POST.get("msg_id"))
        msg.delete()
        return json_response(True, '0', 'success')
    except Msg.DoesNotExist:
        return json_response(False, '020005', "msg does not exist")
    except Exception, e:
        print e
        return json_response(False, '020006', '数据库错误')