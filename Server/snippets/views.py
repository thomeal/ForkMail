import json

from django.http import JsonResponse

from .models import *
from .token import create_token, check_token, get_username


def register(request):
    try:
        req = json.loads(request.body)
        user = User()
        user.mobile = req['username']
        user.nickname = req['nickname']
        user.password = req['password']
        sql = 'select mobile from user where mobile=' + user.mobile
        existed = User.objects.raw(sql)
        if existed:
            raise Exception("该用户已存在")
        user.save()
    except Exception as e:
        return JsonResponse({
            'message': '注册失败',
            'success': 0,
            'error': str(e)
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '注册成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})


def login(request):
    try:
        mobile = request.GET.get('username')
        password = request.GET.get('password')
        sql = 'select * from user where mobile = ' + mobile
        user = User.objects.raw(sql)[0]
        if not user or password != user.password:
            raise Exception("用户名或密码错误")
    except IndexError as ie:
        return JsonResponse({
            'message': '登录失败',
            'success': 0,
            'error': '用户名或密码错误'
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({
            'message': '登录失败',
            'success': 0,
            'error': str(e)
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '登录成功',
            'success': 1,
            'nickname': user.nickname,
            'token': create_token(mobile)
        }, json_dumps_params={'ensure_ascii': False})


def checkAuth(request):
    return JsonResponse({
        'authorized': check_token(request.GET.get('token'))
    }, json_dumps_params={'ensure_ascii': False})


def getMails(request):
    token = request.GET.get('token')
    if check_token(token):
        user = get_username(token)
        token = create_token(user)
#     unfinished


