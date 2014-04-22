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
from liyan.settings import site_name
from liyan.settings import NEED_CONFIRM_EMAIL
from helper.utils import send_email
from helper.utils import generate_register_code
from models import User


@csrf_exempt
@transaction.commit_manually
def register(request):
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST:
        # 已经有数据从前端传回来，用户已填写表单注册
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            new_user = User.objects.create_user(email, username, password)
            active_code = generate_register_code(new_user.id)

            new_user.active_code = active_code
            if not NEED_CONFIRM_EMAIL:
                new_user.is_active = True
            new_user.save()

            url = reverse('accounts:login')
            transaction.commit()
            # 数据库操作成功，事务递交
            return HttpResponseRedirect(url)
        except Exception, e:
            print e
            transaction.rollback()
            # 数据库操作失败，事务回滚
            # 这里继续回到注册页面，并将用户已经填写的非敏感信息返回到前端，方式信息重复填写
            return render_to_response("accounts/register.html",
                                      {'username': username, 'email': email},
                                      context_instance=RequestContext(request))

    else:
        # 尚无数据传回，用户刚打开注册页面
        transaction.rollback()
        # 数据库操作失败，事务回滚
        return render_to_response("accounts/register.html",
                                  context_instance=RequestContext(request))


def active(request, active_code):
    try:
        new_user = User.objects.get(active_code=active_code)
        new_user.is_active = True
        new_user.save()
        return HttpResponseRedirect(reverse('accounts:login'))
    except Exception, e:
        print e
        return render_to_response("accounts/active.html",
                                  {'error': '激活码错误，请重新注册'},
                                  context_instance=RequestContext(request))


@csrf_exempt
def login(request):
    if 'email' in request.POST and 'password' in request.POST:
        # 前台通过POST方式传回username与password两个参数
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # 这里的认证需要的参数username通过setting.py里的AUTH_USER_MODEL进行设置
        user = auth.authenticate(email=email, password=password)
        # 认证成功则登录，使用django自带的login
        if user is not None:
            if not user.is_active:
                active_url = reverse('accounts:re_active', kwargs={'user_id': user.id})
                return render_to_response("accounts/login.html",
                                          {'email': email,
                                           'error': "账户尚未激活，请激活后登陆",
                                           'resend_active_email': active_url},
                                          context_instance=RequestContext(request))
            auth.login(request, user)
            url = reverse("accounts:index")
            return HttpResponseRedirect(url)
        else:
            return render_to_response("accounts/login.html", {'email': email,
                                                              'error': "账户名或密码错误"})
    else:
        return render_to_response("accounts/login.html",
                                  context_instance=RequestContext(request))


def send_active_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        active_code = user.active_code
        active_url = reverse('accounts:active', kwargs={'active_code': active_code})
        send_email("账户激活", "欢迎注册" + site_name + "点击以下链接激活账户" + DOMAIN + active_url, user.email)
        return render_to_response('accounts/re_active.html',
                                  {'error': 0,
                                   'msg': "激活邮件已重新发送直您的邮箱"
                                          + user.email.decode('ascii').encode("utf-8") +
                                          "，请注意查收"},
                                  context_instance=RequestContext(request))
    except User.DoesNotExist:
        return render_to_response('accounts/re_active.html',
                                  {'error': 0,
                                   'error_msg': "用户不存在，请先注册"},
                                  context_instance=RequestContext(request))
    except Exception, e:
        print e
        return render_to_response('accounts/re_active.html',
                                  {'error': 0,
                                   'error_msg': "数据库错误，请重试"},
                                  context_instance=RequestContext(request))


def index(request):
    ret = {}
    if request.user is not None:
        ret['username'] = request.user.username
    return render_to_response("accounts/index.html",
                              ret,
                              context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    # 退出后直接重定向到首页
    url = reverse('accounts:index')
    return HttpResponseRedirect(url)


@csrf_exempt
@login_required()
def check_detail(request):
    if 'username' in request.POST:
        username = request.POST.get('username')
        user = User.objects.get(id=request.user.id)
        user.username = username
        user.save()
        return HttpResponseRedirect("/accounts/")
    else:
        username = request.user.username
        email = request.user.email
        create_time = request.user.create_time
        return render_to_response("accounts/detail.html",
                                  {'username': username,
                                   'email': email,
                                   'create_time': create_time.strftime('%Y-%m-%d'), },
                                  context_instance=RequestContext(request))


@csrf_exempt
@login_required()
def reset_password(request):
    if 'new_password' in request.POST and 'old_password' in request.POST:
        if request.user.check_password(request.POST.get("old_password")):
            request.user.set_password(request.POST.get("new_password"))
            request.user.save()
            return logout(request)
        else:
            return render_to_response("accounts/reset_password.html",
                                      {'error': "旧密码不符"},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response("accounts/reset_password.html",
                                  context_instance=RequestContext(request))