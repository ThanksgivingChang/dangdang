import hashlib
from django.shortcuts import render,HttpResponse,redirect
from login.models import User
import re
# Create your views here.
def login(request):
    '''访问登陆界面'''
    print('this is login.html')
    #获取返回页面地址
    reurl = request.GET.get('returnurl')
    sid = request.GET.get('sid')
    #设置返回的session,先判断如果存在先删除
    rl = request.session.get('reurl')
    if rl:
        del request.session['reurl']
    print(reurl,sid)
    if sid:
        reurl = reurl + '&sid='+str(sid)
    request.session['reurl'] = reurl
    return render(request, 'login/login.html',{'returnurl':reurl})

def login_logic(request):
    '''登陆逻辑'''
    print('this is login_logic')
    #获取返回原界面的reurl
    url = request.session.get('reurl')
    #获取用户email
    email = request.POST.get('email')
    #获取对象
    user = User.objects.filter(email=email)
    res = HttpResponse(url)
    if user:
        #获取盐
        salt=user[0].salt
        #获取密码
        password = request.POST.get('password')
        password = password.lower()
        # 拼接密码
        password = password + salt
        # 转化为二进制字符串
        password = password.encode(encoding='utf-8')
        # 创建哈希对象
        h = hashlib.md5()
        # 生成md5码
        h.update(password)
        # 获取16进制消息炸药
        password = h.hexdigest()
        if password == user[0].password:
            #设置登录nick
            res.set_cookie('user',user[0].nickname,max_age=60*60)
            #设置将用户id存入session
            request.session['gid']=user[0].id
            return res
        else:
            return HttpResponse('0')
    else:
        return HttpResponse('0')

def reemail(request):
    '''正则验证email格式 '''
    #接收email参数
    print('this is remail')
    emi = request.GET.get('email')
    rule = '^[A-Za-z\d]*@[A-Za-z\d]+[\.][A-Za-z\d]{2,4}$'
    confirm = re.findall(rule,emi)
    print(confirm)
    if confirm:
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def logout(request):
    print('this is logout')
    #获取登录标志
    nickname = request.COOKIES.get('user')
    gid = request.session.get('gid')
    #获取登录url
    reurl = request.GET.get('returnurl')
    res = redirect(reurl)
    print(nickname,gid)
    if nickname and gid:
        res.delete_cookie('user')
        del request.session['gid']
    #重定向到原界面
    return res


