import traceback

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from cart.car import CartItem,Cart
from index.models import Product,AddProduct
import json
# Create your views here.



def addproduct(request):
    '''添加商品'''
    print('this is addproduct')
    #接收商品id
    bid = request.GET.get('id')
    #接收商品数量
    amount = int(request.GET.get('amount'))
    print(bid,amount)
    #查询商品
    product = Product.objects.filter(pk=bid)
    #创建一个购物车，获取购物车session，如果存在不创建新的购物车，如果不存在创建一个新的购物车
    cuthand = request.session.get('cuthand')
    # print('ctuhand: ',cuthand)
    if not cuthand:
        hand = Cart()
    else:
        hand = cuthand
    #将商品添加到购物车
    hand.addCartItem(product[0],amount)
    # print('节省：',hand.getSaveMoney(),'总计：',hand.getTotalMoney())
    try:
        #设置session
        cuthand=hand
        # print('即将存入的cuthand',cuthand)
        request.session['cuthand']=cuthand
        #返回加入购物车成功信号
        return HttpResponse(1)
    except:
        traceback.print_exc()

def mycart(request):
    '''访问我的购物车'''
    print('this is mycart')
    #获取登录对象
    nickname = request.COOKIES.get('user')
    #从session获得购物车对象
    cuthand = request.session.get('cuthand')
    # print(cuthand.getSaveMoney())
    # del request.session['cuthand']
    return render(request,'cart/car.html',{'cuthand':cuthand,'nickname':nickname})

def setCartItemAmount(request):
    '''修改订单项数量'''
    print('this is set cartitem amount')
    #接收商品id，接收商品数量
    bookid = int(request.GET.get('id'))
    print(bookid)
    newAmount = int(request.GET.get('amount'))
    print(newAmount)
    #从session获得购物车对象
    cuthand = request.session.get('cuthand')
    #定义mydefault
    def mydefault(a):
        if isinstance(a,CartItem):
            a = { 'amount':a.amount,'product':a.product,'getSubTotal':a.getSubTotal()}
        if isinstance(a,Product):
            a = {'id':a.id}
        if isinstance(a,Cart):
            a = {'getTotalMoney':a.getTotalMoney(),'getSaveMoney':a.getSaveMoney()}
        return a
    for cartItem in cuthand.cartItems:
        if cartItem.product.id == bookid:
            cuthand.setCartItem(cartItem,newAmount)
            #将更新的购物车放入新的session中
            request.session['cuthand'] = cuthand
            #返回新的购物车对象
            return JsonResponse({"cartItem":cartItem,'cuthand':cuthand},json_dumps_params={"default":mydefault})

def delCartItem(request):
    '''删除订单项'''
    print('this is del cartItem')
    # 接收商品id
    bid = request.GET.get('id')
    # 接收商品数量
    print(bid)
    # 查询商品
    product = Product.objects.filter(pk=bid)
    # 获取购物车session
    cuthand = request.session.get('cuthand')
    # print('ctuhand: ',cuthand)
    hand = cuthand
    # 将商品从购物车删除
    hand.subCartItem(product[0])
    # print('节省：',hand.getSaveMoney(),'总计：',hand.getTotalMoney())
    try:
        # 设置session
        cuthand = hand
        # print('即将存入的cuthand',cuthand)
        request.session['cuthand'] = cuthand
        # 重定向到购物车
        return redirect("cart:mycart")
    except:
        traceback.print_exc()

def reCartItem(request):
    '''恢复订单项'''
    print('this is recover cartItem')
    # 接收商品id
    bid = request.GET.get('id')
    # 接收商品数量
    print(bid)
    # 查询商品
    product = Product.objects.filter(pk=bid)
    # 获取购物车session
    cuthand = request.session.get('cuthand')
    # print('ctuhand: ',cuthand)
    hand = cuthand
    # 将商品从购物车删除
    hand.reCartItem(product[0])
    # print('节省：',hand.getSaveMoney(),'总计：',hand.getTotalMoney())
    try:
        # 设置session
        cuthand = hand
        # print('即将存入的cuthand',cuthand)
        request.session['cuthand'] = cuthand
        # 重定向到购物车
        return redirect("cart:mycart")
    except:
        traceback.print_exc()

def trueDelCartItem(request):
    '''彻底删除订单项'''
    print('this is True del cartItem')
    # 接收商品id
    bid = request.GET.get('id')
    # 接收商品数量
    print(bid)
    # 查询商品
    product = Product.objects.filter(pk=bid)
    # 获取购物车session
    cuthand = request.session.get('cuthand')
    # print('ctuhand: ',cuthand)
    hand = cuthand
    # 将商品从购物车彻底删除
    hand.delCartItem(product[0])
    # print('节省：',hand.getSaveMoney(),'总计：',hand.getTotalMoney())
    try:
        # 设置session
        cuthand = hand
        # print('即将存入的cuthand',cuthand)
        request.session['cuthand'] = cuthand
        # 重定向到购物车
        return redirect("cart:mycart")
    except:
        traceback.print_exc()