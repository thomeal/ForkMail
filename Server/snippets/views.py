import json

import chardet
from django.http import JsonResponse

from .mail import MailAccount
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
            'success': 0,
            'message': '用户名或密码错误'
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({
            'success': 0,
            'message': str(e)
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '登录成功',
            'success': 1,
            'nickname': user.nickname,
            'token': create_token(mobile),
            'mobile': mobile
        }, json_dumps_params={'ensure_ascii': False})


def addMailBox(request):
    req = json.loads(request.body)
    token = req['token']
    mail = Email()
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        # else:
        user = get_username(token)
        mail.email = req['email']
        mail.key = req['key']
        mail.smtp_host = req['smtpHost']
        mail.imap_host = req['imapHost']
        mail.user = User.objects.raw('select * from user where mobile = ' + user)[0]
        sql = 'select email from email where email = \'' + mail.email + '\''
        existed = Email.objects.raw(sql)[0]
        if existed:
            raise Exception("该邮箱已经被占用")
    except IndexError as ie:
        mail.save()
        return JsonResponse({
            'message': '添加成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '添加失败',
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})


def deleteMailBox(request):
    req = json.loads(request.body)
    token = req['token']
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        user = get_username(token)
        email = req['email']
        sql = 'select * from email where email=' + email
        existed = Email.objects.raw(sql)[0]
        if not existed or existed.user.mobile != user:
            raise Exception("您没有该邮箱")
        existed.delete()
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '删除成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})


def editMailBox(request):
    req = json.loads(request.body)
    token = req['token']
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        user = get_username(token)
        email = req['email']
        key = req['key']
        sql = 'select * from email where email=' + email
        mail = Email.objects.raw(sql)[0]
        if not mail or mail.user.mobile != user:
            raise Exception("您没有该邮箱")
        mail.key = key
        mail.save()
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '修改成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})


def getMailBoxes(request):
    token = request.GET.get('token')
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        user = get_username(token)
        mail_boxes = list(Email.objects.filter(user=user).values_list('email', flat=True))
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '操作成功',
            'success': 1,
            'mailBoxes': mail_boxes,
        }, json_dumps_params={'ensure_ascii': False})


def deleteMail(request):
    req = json.loads(request.body)
    token = req['token']
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        user = get_username(token)
        account = Email.objects.raw("select * from email where email = " + req['mail'])[0]
        uid = req['id']
        if account.user.mobile != user:
            raise Exception('您的账号名下没有该邮箱')
        MailAccount(account=account).deleteMail(uid)
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '删除成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})


def sendMail(request):
    req = json.loads(request.body)
    token = req['token']
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        # else:
        user = get_username(token)
        account = Email.objects.raw("select * from email where email = " + req['mail'])[0]
        if account.user.mobile != user:
            raise Exception('您的账号名下没有该邮箱')
        MailAccount(account=account).send_email_by_smtp(req['receiver'], req['subject'], req['content'])
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'message': '发送成功',
            'success': 1,
        }, json_dumps_params={'ensure_ascii': False})


def getMails(request):
    token = request.GET.get('token')
    if not check_token(token):
        return JsonResponse({
            'message': '认证失败，需要重新登录',
            'success': 0,
            'reLoginRequired': 1
        }, json_dumps_params={'ensure_ascii': False})
    try:
        # else:
        user = get_username(token)
        account = Email.objects.raw("select * from email where email = " + request.GET.get('mail'))[0]
        if account.user.mobile != user:
            raise Exception('您的账号名下没有该邮箱')
        mails = MailAccount(account=account).getAllMails()
        mail_list = list()
        for uid, message in mails:
            if not message.body['html']:
                html = ''
            elif isinstance(message.body['html'][0], str):
                html = message.body['html'][0]
            else:
                encoding = chardet.detect(message.body['html'][0])
                html = message.body['html'][0].decode(encoding['encoding'])
            if not message.body['plain']:
                plain = ''
            elif isinstance(message.body['plain'][0], str):
                plain = message.body['plain'][0]
            else:
                encoding = chardet.detect(message.body['plain'][0])
                plain = message.body['plain'][0].decode(encoding['encoding'])
            if hasattr(message, 'date'):
                mail_list.append({
                    'sender': str(message.sent_from),
                    'receiver': str(message.sent_to),
                    'subject': str(message.subject),
                    'header': str(message.headers),
                    'date': str(message.date),
                    'html': html,
                    'plain': plain,
                    'id': uid.decode(),
                })
            else:
                mail_list.append({
                    'sender': str(message.sent_from),
                    'receiver': str(message.sent_to),
                    'subject': str(message.subject),
                    'header': str(message.headers),
                    'html': html,
                    'plain': plain,
                    'id': uid.decode(),
                })
        return JsonResponse({
            'message': '操作成功',
            'success': 1,
            'mail': mail_list,
            'token': token
        }, json_dumps_params={'ensure_ascii': False})
    except IndexError as ie:
        return JsonResponse({
            'message': '您的账号名下没有该邮箱',
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({
            'message': str(e),
            'success': 0,
        }, json_dumps_params={'ensure_ascii': False})
