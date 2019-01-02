import random
import re
import traceback
import hashlib
import string

from django.db import transaction
from django.shortcuts import render,HttpResponse
from login.models import User
from register.captcha.image import ImageCaptcha
from django.core.mail import send_mail


#fuction


def getsalt():
    l='~!@#$%^&*()_+}|{P":?><QWERTYUIOASDFGHHJKLZXCVBNM,./;[]\=-0987654321asdfghjhklopiuytrewq'
    salt=''.join(random.sample(l,6)).replace(" ","")
    return salt

def getemailcode():
    codepool='1234567890'
    securitycode = ''.join(random.sample(codepool,6))
    return securitycode

# Create your views here.

def register(request):
    '''访问注册界面'''
    print('this is register.html')
    #获取返回url
    reurl = request.GET.get('returnurl')
    sid = request.GET.get('sid')
    # 设置返回的session,先判断如果存在先删除
    rl = request.session.get('reurl')
    if rl:
        del request.session['reurl']
    print(reurl, sid)
    if sid:
        reurl = reurl + '&sid=' + str(sid)
    if not reurl:
        reurl='/DangDang/index/'
    request.session['reurl'] = reurl
    return render(request,'register/register.html')

def register_logic(request):
    '''注册逻辑'''
    #获取验证码和邮箱session
    checkcaptcha = request.session.get('checkcaptcha')
    checkremail = request.session.get('checkremail')
    if checkcaptcha and checkremail:
        #获取email,password,nick
        flag = 0
        print('this is register_logic')
        confrim_email = request.session.get('email')
        if confrim_email:
            del request.session['email']
        email = request.POST.get('email')
        email = email.lower()
        #获取密码
        password = request.POST.get('password')
        password = password.lower()
        #获取随机盐
        salt=getsalt()
        #拼接密码
        password = password+salt
        #转化为二进制字符串
        password = password.encode(encoding='utf-8')
        #创建哈希对象
        h= hashlib.md5()
        #生成md5码
        h.update(password)
        #获取16进制消息炸药
        password=h.hexdigest()
        print(password)
        nick = request.POST.get('nick')
        print(email,password,nick)
        try:
            with transaction.atomic():
                user = User(email=email,password=password,nickname=nick,salt=salt,status=1)
                user.save()
        except Exception:
            traceback.print_exc()
        else:
            flag = 1
        if flag:
            res = HttpResponse(1)
            request.session['email'] = email
            res.set_cookie('user',nick, max_age=60*60)
            request.session['gid'] = 1
            return res
        else:
            return HttpResponse(0)
    else:
        return HttpResponse(0)


def register_success(request):
    '''访问注册成功界面'''
    print('this is register_success.html')
    email=request.session.get('email')
    # 获取返回原界面的reurl
    url = request.session.get('reurl')
    return render(request,'register/register ok.html',{'email':email,'url':url})

def email_check(request):
    '''邮箱验证'''
    print('this is email_check')
    email=request.session.get('email')
    emaillist=[]
    emaillist.append(email)
    #生成邮箱验证码
    scode = getemailcode()
    # 将验证码存入session
    if request.session.get('scode'):
        del request.session['scode']
    else:
        request.session['scode'] = scode
    #将验证码发送到指定邮箱
    send_mail('知之网邮箱验证码','感谢您使用知之网，您的激活码为'+scode,'zblhappy12@163.com',emaillist)
    return render(request,'register/register_email_check.html',{'email':email})

def email_checklogic(request):
    '''邮箱验证逻辑'''
    #获取接收的邮箱验证码
    mcode = request.GET.get('estc')
    #获取session中生成的验证码
    scode = request.session.get('scode')
    if mcode == scode:
        return HttpResponse(1)
    else:
        return  HttpResponse(0)

def reemail(request):
    '''正则验证email格式 '''
    #接收email参数
    print('this is remail')
    if request.session.get('checkremail'):
        del request.session['checkremail']
    emi = request.GET.get('email')
    rule = '^[A-Za-z\d]*@[A-Za-z\d]+[\.][A-Za-z\d]{2,4}$'
    confirm = re.findall(rule,emi)
    print(confirm)
    if confirm:
        user = User.objects.filter(email=emi)
        request.session['checkremail']=1
        if user:
            del request.session['checkremail']
            return HttpResponse(3) #邮箱格式正确但是已经被注册
        return HttpResponse(1) #邮箱格式正确未被注册
    else:
        return HttpResponse(0) #邮箱格式错误

def pinSecurity(request):
    '''密码验证'''
    print('this is pin security')
    #获取密码
    pwd = request.GET.get('pwd')
    #如果密码小于6位或者是有单一元素组成：简单
    #如果密码大于等于8 小于16 并且是由字母/数字/特殊字符组成，：中
    #密码必须有三种字符组成且长度大于8
    o,s,t=0,0,0
    for i in pwd:
        if i.isalpha():
            o=1
        elif i.isalnum():
            s=1
        else:
            t =1
    num=o+s+t
    if num==1 or len(pwd)<=6:
        return  HttpResponse(1)
    elif num==2:
        return HttpResponse(2)
    elif num==3:
        return HttpResponse(3)

def getcaptcha(request):
    print('this is getcaptcha')
    image = ImageCaptcha()
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 4)
    random_code = "".join(code)
    print(random_code)
    request.session['code'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data, "image/png")

def checkCaptcha(request):
    print('this is checkcaptcha')
    if request.session.get('checkcaptcha'):
        del request.session['checkcaptcha']
    #获取session验证码
    bt_code = request.session.get('code')
    #获取输入验证码
    up_code = request.GET.get('code')
    print(bt_code,up_code)
    if up_code.lower() == bt_code.lower():
        request.session['checkcaptcha']=1
        return HttpResponse(1)
    else:
        return HttpResponse(0)
