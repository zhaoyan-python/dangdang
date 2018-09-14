import hashlib
import random
import re
import string
import traceback

from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.d
from captcha.image import ImageCaptcha
from user_app.models import TUser
def regist_page(request):
    #请求场景：
    # 首页注册：加一个flag：0
    # 登陆页面：加一个flag：1
    #接收参数flag,将其出入session中，注册成功页面使用：
    return render(request,'user_app/register.html')
def name_check(request):
    #接收请求参数：
    user_name=request.POST.get('user_name')
    print(user_name)
    #验证name格式：
    result=re.search('(^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$)|(1[34578]\d{9})|(\+?\d{3,4}-?\d{7,8})|(\+\(\d\)(\d{3}-){2}\d{3})',user_name)
    if not result:
        return HttpResponse('0')
    else:
        # 查表验证name是否重复：
        user=TUser.objects.filter(user_name=user_name)
        if user:
            return HttpResponse('1')
        else:
            return HttpResponse('2')
#获取验证码：
def get_captcha(request):
    img=ImageCaptcha()
    code=random.sample(string.ascii_letters+string.digits,4)
    random_code=''.join(code)
    request.session['random_code']=random_code
    data=img.generate(random_code)
    return HttpResponse(data,'image/png')
#验证验证嘛
def check_captcha(request):
    #获取参数：
    captcha=request.GET.get('captcha')
    if request.session.get('random_code').lower()==captcha.lower():
        return HttpResponse('2')
    return HttpResponse('1')
#获取yan
def get_salt():
    l='!@#$%^&*()<>?":QWERTYUIOasdghjllzxcvbnm'
    salt=''.join(random.sample(l,4)).replace(' ','')
    return salt
def get_pwd(pwd,salt=None):
    h=hashlib.md5()
    h.update((pwd+salt).encode())
    return h.hexdigest()
def regist_logic(request):
    # 请求场景：略u
    #接收参数：
    user_name=request.POST.get('txt_username')
    password=request.POST.get('txt_password')
    print(password,user_name)
    #session 中存入user_name:register_ok_page备用：
    request.session['user_name']=user_name
    #密码加密：
    salt=get_salt()
    password=get_pwd(password,salt)
    #存储数据：
    try:
        with transaction.atomic():
            print(user_name,password,salt)
            TUser(user_name=user_name,password=password,salt=salt).save()
    except:
        traceback.print_exc()
    #跳转到注册成功页面：
    return redirect('user_app:regist_ok_page')
def regist_ok_page(request):
    #请求场景：略
    #自动登陆，session 中存储登陆状态
    return render(request,'user_app/register ok.html')
def login_page(request):
    #需求场景：1，首页，2，注册页面，3强制登陆：
    return render(request,'user_app/login.html')
def login_logic(request):
    #获取参数；
    user_name=request.POST.get('user_name')
    password=request.POST.get('password')
    #查询为user_name的对象：
    print(user_name)
    request.session['user_name'] = user_name
    print(request.session.get('user_name'))

    user=TUser.objects.filter(user_name=user_name)
    #判断user：
    if not user:
        return HttpResponse('0')
    else:
        #查询salt:
        salt=user[0].salt
        #密码加密：
        password=get_pwd(password,salt)
        #if 判断you返回为1,没有返回0；
        if user[0].password==password:
            request.session['user_name'] = user_name
            return HttpResponse('1')
        else:
            return HttpResponse('0')
def send_email(request):
    random_code=random.sample(string.ascii_letters+string.digits,4)
    recipient=request.GET.get('email')
    code=''.join(random_code).replace(' ','')
    send_mail('验证码',code,'zy4200074390@163.com',[recipient])
    return HttpResponse(code)
