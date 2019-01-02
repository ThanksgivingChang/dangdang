from django.core.paginator import Paginator
from django.db.models import Max, F
from django.http import HttpResponse
from django.shortcuts import render
from  index.models import Menus,AddProduct,Product
# Create your views here.
#冒泡排序
def orderby(books):
    '''传入一个books列表'''
    pass
def dangdang(request):
    '''首页展示'''
    print('this is dangdang.index')
    apros=[]
    heditors=[]
    #获取用户nickname
    nickname = request.COOKIES.get('user')
    #查询图书分类
    fathers = Menus.objects.filter(parent=0)
    sons = Menus.objects.filter(parent__gt=0)
    #查询新书上架，需要对书籍分页
    pagtor = AddProduct.objects.filter(issue__gt='2018-9-1')
    for parange in Paginator(pagtor,per_page=8).page_range:
        apros.append(Paginator(pagtor,per_page=8).page(parange))
    #查询热卖新书，排序并分页
    pagtor2 = pagtor.order_by('-sales')
    apros2 = Paginator(pagtor2,per_page=10).page(1)
    #查询主编推荐，需要对书籍分页
    paeditor = AddProduct.objects.filter(recommand=1)
    for parange2 in Paginator(paeditor,per_page=10).page_range:
        heditors.append(Paginator(paeditor,per_page=10).page(parange2))
    #查询畅销图书，排序并分页
    pagtor3= AddProduct.objects.all().order_by('-sales')
    apros3 = Paginator(pagtor3, per_page=10).page(1)
    return render(request, 'index/index.html',{'fathers':fathers,'sons':sons,'apros':apros,'apros2':apros2,'heditors':heditors,'apros3':apros3,'nickname':nickname})

def bookdetails(request):
    '''详情页展示'''
    print('this is bookdetails')
    # 获取用户nickname
    nickname = request.COOKIES.get('user')
    #获取书籍编号
    book_id = request.GET.get('id')
    print(book_id)
    book_id= int(book_id)
    #查询书籍
    book=Product.objects.get(pk=book_id)
    #计算书籍折扣
    zhekou = book.addproduct.dangdang_price*10/book.addproduct.price
    #查询所有一级分类
    bookcategory=Menus.objects.filter(parent=0)
    return render(request,'index/Book details.html',{'book':book,'zhekou':zhekou,'cate':bookcategory,'nickname':nickname})

def booklist(request):
    '''分类页展示'''
    print('this is booklist')
    # 获取用户nickname
    nickname = request.COOKIES.get('user')
    book_list=[]
    #接收参数：pid,sid
    pid = request.GET.get('pid')
    sid = request.GET.get('sid')
    pg = request.GET.get('page')
    filed = request.GET.get('filed')
    isdesc = request.GET.get('isdesc')
    print(pid,sid,pg,filed)
    # 查询图书分类
    fathers = Menus.objects.filter(parent=0)
    sons = Menus.objects.filter(parent__gt=0)
    #查询当前页具体类别
    try:
        c_father = Menus.objects.get(pk=pid) #如果pid不存在，返回第一个一级分类标签
    except Exception:
        c_father = Menus.objects.get(pk=1)
    if sid:
        c_son = Menus.objects.filter(pk=sid) #如果sid不存在，返回该一级分类下所有二级分类
    else:
        c_son = Menus.objects.filter(parent=c_father.id)
    #查询c_son分类下所有书籍
    if filed:
        if isdesc == '1':
            for cs in c_son:
                for book in cs.product_set.all():
                    book_list.append(book)
            #冒泡排序
        else:
            print(2)
            filed = '-' + filed
            if filed == '-sales':
                for cs in c_son:
                    for book in cs.product_set.addprodeuct.all().order_by(filed):
                        book_list.append(book)
            elif filed == '-publishing_time':
                print(1)
                for cs in c_son:
                    for book in cs.product_set.all().order_by(filed):
                        book_list.append(book)
    else:
        for cs in c_son:
            for book in cs.product_set.all():
                book_list.append(book)
    #对查询到的书籍进行分页
    books_paginator = Paginator(book_list,per_page=6)
    try:
        books = books_paginator.page(pg)
    except Exception:
        books = books_paginator.page(1)
    if books.paginator.num_pages <= 6:
        pages_range=None
    else:
        pages_range = range(1,7)
    return render(request,'index/booklist.html',{'fathers':fathers,'sons':sons,'c_father':c_father,'c_son':c_son,'books':books,'pages_range':pages_range,'nickname':nickname})

def booktest(request):
    print('this is book  test')
    product = Product.objects.filter(isbn__gt=F('word'))
    print(product)
    return HttpResponse('ok')