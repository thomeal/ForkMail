import json

from django.http import JsonResponse

from .mail import *
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
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    try:
        user = get_username(token)
        # token = create_token(user)
        account = Email.objects.raw('select * from email where email = ' + request.GET.get('mail'))[0]
        if account.user.mobile != user:
            raise Exception('您的账号名下没有该邮箱')
        mails = MailAccount(account=account).getAllMails()
        mail_list = list(0 for i in range(mails.__len__()))
        i = 0
        for uid, message in mails:
            if hasattr(message,'date'):
                mail_list[i] = {
                    'sender': message.sent_from,
                    'receiver': message.sent_to,
                    'subject': message.subject,
                    'header': message.headers,
                    'date': message.date,
                    'html': message.body['html'],
                    'plain': message.body['plain'],
                    'attachments': message.attachments
                }
            else:
                mail_list[i] = {
                    'sender': message.sent_from,
                    'receiver': message.sent_to,
                    'subject': message.subject,
                    'header': message.headers,
                    'html': message.body['html'],
                    'plain': message.body['plain'],
                    'attachments': message.attachments
                }
            i += 1
        return JsonResponse({
            'message': '操作成功',
            'success': 0,
            'mail': mail_list.__str__(),
            'token': token
        }, json_dumps_params={'ensure_ascii': False})
    # except IndexError as ie:
    #     return JsonResponse({
    #         'message': '您的账号名下没有该邮箱',
    #         'success': 0,
    #         'token': token
    #     }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        # return JsonResponse({
        #     'message': str(e),
        #     'success': 0,
        #     'token': token
        # }, json_dumps_params={'ensure_ascii': False})
        raise e
