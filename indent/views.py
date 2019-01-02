import random

import time
import traceback

from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from login.models import User
from indent.models import Address,Orders,OrderItems
from index.models import Product,AddProduct

from cart.car import Cart,CartItem

# Create your views here.
from django.urls import reverse

def getsalt():
    '''订单盐'''
    l='0987654321'
    t='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLLZXCVBNM'
    salt_body=''.join(random.sample(l,8)).replace(" ","")
    salt_head=''.join(random.sample(t,4)).replace(" ","")
    salt = salt_head + salt_body + str(int(time.time()))
    return salt

def freight(cuthand):
    '''计算运费'''
    try:
        if cuthand.getTotalMoney() > 100:
            return 0
        else:
            return 10
    except TypeError:
        return 1

def getindent(request):
    '''访问订单页'''
    print('this is get indent')
    #获取登录gid
    gid = request.session.get('gid')
    #获取nickname
    nickname = request.COOKIES.get('user')
    if gid and nickname:
        gid=int(gid)
        #获取购物车对象
        cuthand = request.session.get('cuthand')
        #查询该用户的地址信息
        address = Address.objects.filter(userid=gid)
        print('地址信息',address)
        #获取运费
        fght = freight(cuthand)
        if fght == 1:
            return redirect('cart:mycart')
        #总金额
        totalprice = fght+cuthand.getTotalMoney()
        print(nickname,gid)
        print(cuthand,fght)
        # 查询该用户的地址信息
        address = Address.objects.filter(userid=gid)
        print(address)
        return render(request, 'indent/indent.html', {'nickname': nickname, 'cuthand': cuthand, 'totalprice': totalprice, 'address': address})
    else:
        url = reverse('log:login')+'?returnurl='+reverse('ind:get')
        return HttpResponseRedirect(url)

def indent_logic(request):
    print('this is indent logic')
    #获取订单项session.如果存在删除
    order = request.session.get('order')
    if order:
        del request.session['order']
    #获取登录gid
    gid = int(request.session.get('gid'))
    #查询用户
    guser=User.objects.get(pk=gid)
    #获取购物车对象
    cuthand = request.session.get('cuthand')
    #获取form表单对象
        #获取地址信息
    adrs_flag = int(request.POST.get('address'))
    print(adrs_flag)
    try:
        with transaction.atomic():
            if adrs_flag == -1:
                #获取收货人
                consignee = request.POST.get('ship_man')
                #获取详细地址
                dtas = request.POST.get('detailAddress')
                #获取邮编
                ptle = request.POST.get('postalcode')
                #获取手机号
                mph = request.POST.get('mobilephone')
                #获取固定电话
                tph = request.POST.get('telephone')
                print('收货人：',consignee,'详细地址：',dtas,'邮政编码：',ptle,'手机号：',mph,'固定电话：',tph,'用户id：',gid)
                #创建地址对象,判断地址对象存不存在
                address = Address(consignee=consignee,detailAddress=dtas,postalcode=ptle,telephone=tph,mobilephone=mph,userid=guser)
                address.save()
            else:
                address = Address.objects.filter(id=adrs_flag,userid=gid)[0]
    except:
        traceback.print_exc()
    try:
        with transaction.atomic():
            #获取订单盐
            salt = getsalt()
            #获取当前时间
            dip = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            #获取运费
            fght = freight(cuthand)
            #获取总金额
            totalprice = fght+cuthand.getTotalMoney()
            #创建订单对象
            print('订单号：',salt,'订单时间：',dip,'运费：',fght,'总金额：',totalprice)
            newOrders = Orders(orderNumber=salt,dateInProduct=dip,status=0,freight=fght,expenditure=totalprice,customer=guser,address=address)
            #持久化
            newOrders.save()
            #存入session
            request.session['order']=newOrders
    except:
        traceback.print_exc()
    try:
        with transaction.atomic():
            cartFlag=[]
            for one in cuthand.cartItems:
                cartFlag.append(one)
                productName = one.product.name
                price= one.product.addproduct.dangdang_price
                amount=one.amount
                subtotal=one.getSubTotal()
                print('商品：',productName,'价格：',price,'数量：',amount,'小计：',subtotal)
                newOrderItems=OrderItems(productName=productName,price=price,amount=amount,subtotal=subtotal,orderid=newOrders)
                newOrderItems.save()
                #更新商品销售数据
                aproduct = AddProduct.objects.get(product_id__id=one.product.id)
                aproduct.sales = aproduct.sales+amount
                aproduct.save()
                print('sales:',aproduct.sales)
            print('cartFlag:',cartFlag)
            request.session['cartFlag']=cartFlag
    except:
        traceback.print_exc()

    return HttpResponse(1)

def retindent(request):
    '''访问订单已生产界面'''
    print('this is return indent')
    #获取nickname
    nickname = request.COOKIES.get('user')
    #获取session中的order
    order = request.session.get('order')
    #获取购物车
    cuthand = request.session.get('cuthand')
    #将购物车中的订单项去除,获取cartFlag
    cartFlag = request.session.get('cartFlag')
    print('删除前：',cuthand.cartItems,cuthand.uncartItems)
    if cartFlag:
        for one in cartFlag:
            #将购物车中的订单项移入删除模块
            cuthand.subCartItem(one.product)
        print('删除中：',cuthand.cartItems,cuthand.uncartItems)
        for one in cartFlag:
            #删除购物车中删除模块中的订单项
            cuthand.delCartItem(one.product)
        print('删除后：',cuthand.cartItems,cuthand.uncartItems)
    # 获取移出商品的记录，并将移出商品添加到购物车中
    delproduct = request.session.get('delproduct')
    if delproduct:
        for one in delproduct:
            cuthand. reCartItem(one)
        del request.session['delproduct']
    print('检查购物车：',cuthand.cartItems,cuthand.uncartItems)
    request.session['ctuhand']=cuthand
    return render(request,'indent/indent ok.html',{'order':order,'nickname':nickname})

def setaddress(request):
    '''异步刷新地址栏'''
    print('this is set address')
    #获取地址id
    adid = request.GET.get('adid')
    #查询地址对象
    adrs = Address.objects.filter(pk=adid)
    def mydefault(a):
        if isinstance(a,Address):
            a ={'id':a.id,'consignee':a.consignee,'detailAddress':a.detailAddress,'postalcode':a.postalcode,'telephone':a.telephone,'mobilephone':a.mobilephone}
        return a
    if adrs:
        address=adrs[0]
        return JsonResponse({'address':address},json_dumps_params={'default':mydefault})
    else:
        return HttpResponse(-1)

def backToCart(request):
    print('this is back to cart')
    #判断是否存在移出商品记录,没有则创建新的记录list
    delproduct = request.session.get('delproduct')
    if not delproduct:
        delproduct = []
    #获取商品id
    id = int(request.GET.get('id'))
    #查询商品
    product = Product.objects.get(pk=id)
    #获取购物车对象
    cuthand = request.session.get('cuthand')
    #将要删除的商品从当前购物车的cartItems移入uncartItems,保留移出商品的记录
    cuthand.subCartItem(product)
    #保存记录,并存入session
    delproduct.append(product)
    request.session['delproduct']=delproduct
    #保存新的购物车
    request.session['cuthand']=cuthand
    #返回购物车对象
    # def mydefault(a):
    #     if isinstance(a, Cart):
    #         a = {'getTotalMoney': a.getTotalMoney(), 'getSaveMoney': a.getSaveMoney(),'cartItems':a.cartItems}
    #     if isinstance(a, CartItem):
    #         a = {'amount': a.amount, 'product': a.product, 'getSubTotal': a.getSubTotal()}
    #     if isinstance(a, Product):
    #         a = {'id': a.id,'publishing_house':a.publishing_house,'addproduct':a.addproduct}
    #     if isinstance(a, AddProduct):
    #         a = {'dangdang_prcie': a.dangdang_price}
    #     return a
    # return JsonResponse({'cuthand':cuthand},json_dumps_params={"default":mydefault})
    return HttpResponse(1)




