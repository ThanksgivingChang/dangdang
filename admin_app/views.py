import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from index.models import Product,AddProduct,Menus
from indent.models import Address
from login.models import User

# Create your views here.
def getadmin(request):
    '''访问后台管理系统'''
    print('this is admin complie')
    return render(request,'admin_app/index.html')

def addproduct(request):
    '''增加商品'''
    print('this is add product')
    #获取增加成功标志
    success = request.session.get('addsuccess')
    print(success)
    # 删除添加成功标志
    if success:
        del request.session['addsuccess']
    #获取所有父类别
    parentcategory=Menus.objects.filter(parent=0)
    return render(request,'admin_app/main/add.html',{'parentcategory':parentcategory,'success':success})

def addproduct_logic(request):
    '''增加商品逻辑'''
    print('this is add product logic')
    #删除添加成功标志
    success = request.session.get('addsuccess')
    if success:
        del request.session['addsuccess']
    #获取form表单信息
    name=request.POST.get('name')
    author = request.POST.get('author')
    face = request.FILES.get('face')
    publishing_house = request.POST.get('publishing_house')
    edition = request.POST.get('edition')
    publishing_time =request.POST.get('publishing_time')
    print_time = request.POST.get('print_time')
    isbn = request.POST.get('isbn')
    word = request.POST.get('word')
    number_of_page = request.POST.get('number_of_page')
    format_of_book = request.POST.get('format_of_book')
    paper_size = request.POST.get('paper_size')
    packaging = request.POST.get('packaging')
    procate = request.POST.get('procate')
    status = request.POST.get('status')
    print('name:',name,'author:',author,'face:',face,'publishing_house:',publishing_house,'edition:',edition,'\n',
          'publishing_time:',publishing_time,'print_time:',print_time,'isbn:',isbn,'word:',word,'number_of_page:', number_of_page,'\n',
          'format_of_book',format_of_book,'paper_size:',paper_size,'packaging:',packaging,'procate:',procate,'status:',status)
    sales=request.POST.get('sales')
    price = request.POST.get('price')
    dangdang_price = request.POST.get('dangdang_price')
    score = request.POST.get('score')
    issue = request.POST.get('issue')
    recommand = request.POST.get('recommand')
    print('sales:',sales,'price:',price,'dangdang_prcie:',dangdang_price,'score:',score,'issue:',issue,'recommand:',recommand)
    #查询二级类别对象
    if procate:
        procate=int(procate)
        menu=Menus.objects.get(pk=procate)
        with transaction.atomic():
            #创建Product对象
            newProduct=Product(name=name,author=author,face=face,publishing_house=publishing_house,edition=edition,
                               publishing_time=publishing_time,print_time=print_time,isbn=isbn,word=word,
                               number_of_page=number_of_page,format_of_book=format_of_book,paper_size=paper_size,
                               packaging=packaging,status=status,menus=menu)
            newProduct.save()
            #创建AddProduct对象
            newAddProduct = AddProduct(sales=sales,price=price,dangdang_price=dangdang_price,score=score,issue=issue,recommand=recommand,product_id=newProduct)
            newAddProduct.save()
            #存入添加成功标志
            request.session['addsuccess']=1
    return redirect('adm:add')

def subproduct(request):
    '''删除商品'''
    print('this is sub product')
    #获取商品ID
    bid = int(request.GET.get('id'))
    with transaction.atomic():
        #查询商品
        product = Product.objects.get(pk=bid)
        print(product)
        #删除商品将商品的状态置为2
        product.status ='2'
        product.save()
    #返回商品列表
    return redirect('adm:prolist')

def setproduct(request):
    '''修改商品界面'''
    print('this is set product')
    #获取商品id
    bid = int(request.GET.get('id'))
    #查询商品
    product = Product.objects.get(pk=bid)
    # 获取所有父类别
    parentcategory = Menus.objects.filter(parent=0)
    #将商品id存入session
    request.session['set']=bid
    return render(request,'admin_app/main/setlist.html',{'product':product,'parentcategory':parentcategory})

def setproduct_logic(request):
    '''修改商品逻辑'''
    print('this is set product logic')
    #获取商品id
    bid = int(request.session.get('set'))
    #获取商品
    products= Product.objects.get(pk=bid)
    # 获取form表单信息
    name = request.POST.get('name')
    author = request.POST.get('author')
    face = request.FILES.get('face')
    publishing_house = request.POST.get('publishing_house')
    edition = request.POST.get('edition')
    publishing_time = request.POST.get('publishing_time')
    print_time = request.POST.get('print_time')
    isbn = request.POST.get('isbn')
    word = request.POST.get('word')
    number_of_page = request.POST.get('number_of_page')
    format_of_book = request.POST.get('format_of_book')
    paper_size = request.POST.get('paper_size')
    packaging = request.POST.get('packaging')
    procate = request.POST.get('procate')
    status = request.POST.get('status')
    print('name:', name, 'author:', author, 'face:', face, 'publishing_house:', publishing_house, 'edition:', edition,'\n',
          'publishing_time:', publishing_time, 'print_time:', print_time, 'isbn:', isbn, 'word:', word,
          'number_of_page:', number_of_page, '\n',
          'format_of_book', format_of_book, 'paper_size:', paper_size, 'packaging:', packaging, 'procate:', procate,
          'status:', status)
    sales = request.POST.get('sales')
    price = request.POST.get('price')
    dangdang_price = request.POST.get('dangdang_price')
    score = request.POST.get('score')
    issue = request.POST.get('issue')
    recommand = request.POST.get('recommand')
    print('sales:', sales, 'price:', price, 'dangdang_prcie:', dangdang_price, 'score:', score, 'issue:', issue,
          'recommand:', recommand)
    # 查询二级类别对象
    if procate:
        procate = int(procate)
        menu = Menus.objects.get(pk=procate)
        with transaction.atomic():
            # 更新Product对象
            products.name=name
            products.author=author
            products.face=face
            products.publishing_house=publishing_house
            products.edition=edition
            products.publishing_time=publishing_time
            products.print_time=print_time
            products.isbn=isbn
            products.word=word
            products.number_of_page=number_of_page
            products.format_of_book=format_of_book
            products.paper_size=paper_size
            products.packaging=packaging
            products.status=status
            products.menus=menu
            # 通过类属性名更新AddProduct对象
            products.addproduct.sales=sales
            products.addproduct.price=price
            products.addproduct.dangdang_price=dangdang_price
            products.addproduct.score=score
            products.addproduct.issue=issue
            products.addproduct.recommand=recommand
            products.save()
            products.addproduct.save()
    return redirect('adm:prolist')

def productlist(request):
    '''商品列表'''
    print('this is product list')
    #获取跳转页码
    num = request.GET.get('num')
    #查询所有商品
    products = Product.objects.all()
    #分页
    paginetor = Paginator(products,per_page=25)
    try:
        num=int(num)
        pages = paginetor.page(num)
    except:
        pages = paginetor.page(1)
    return render(request,'admin_app/main/list.html',{'pages':pages})

def addparentcategory(request):
    '''增加商品父类别'''
    print('this is add parent category')
    return render(request,'admin_app/main/zjsp.html')

def addparentcategory_logic(request):
    '''增加商品父类别分类'''
    print('this is add parent category logic')
    #接收父类别名称
    newcategory = request.GET.get('cate')
    #查询语句
    category = Menus.objects.filter(parent=0)
    for one in category:
        if one.name == newcategory:
            return HttpResponse(0)
    else:
        #创建新的父类
        with transaction.atomic():
            newMenus = Menus(name=newcategory,parent=0)
            newMenus.save()
        return HttpResponse(1)

def addsoncategory(request):
    '''增加商品子类别'''
    print('this is add son category')
    #查出所有的父类
    parentcategory = Menus.objects.filter(parent=0)
    return render(request,'admin_app/main/zjzlb.html',{"parentcategory":parentcategory})

def addsoncategory_logic(request):
    '''增加商品子类别逻辑'''
    print('this is add son category logic')
    #获取参数
    cate = request.GET.get('cate')
    fid = request.GET.get('fid')
    category = Menus.objects.filter(parent=fid,name=cate)
    if category:
        return HttpResponse(0)
    else:
        #创建新类别
        with transaction.atomic():
            newMenus = Menus(name=cate,parent=fid)
            newMenus.save()
        return HttpResponse(1)

def delcategory(request):
    '''删除类别'''
    print('this is delete category')
    #获取类别id
    cid = int(request.GET.get('cid'))
    #检查是不是一级类别
    menus = Menus.objects.get(pk=cid)
    if menus.parent:
        #是二级类别直接删除
        menus.delete()
        return redirect('adm:ctlt')
    else:
        #是一级类别，查询所有二级类别
        secondmenus=Menus.objects.filter(parent__gt=0)
        with transaction.atomic():
            menus.delete()
            for one in secondmenus:
                if one.parent == cid:
                    one.parent = None
                    one.save()
        return redirect('adm:ctlt')

def categorylsit(request):
    '''商品类别表'''
    print('this is category list')
    #获取跳转页码
    num = request.GET.get('num')
    #查询商品所有类别
    categorys = Menus.objects.all()
    #对类别进行分页
    paginator = Paginator(categorys,per_page=20)
    try:
        num = int(num)
        pages = paginator.page(num)
    except:
        pages = paginator.page(1)
    return render(request,'admin_app/main/splb.html',{'pages':pages})

def addresslist(request):
    '''地址表'''
    print('this is address list')
    #获取跳转页码
    num = request.GET.get('num')
    #查询所有地址信息
    address = Address.objects.all()
    #分页
    paginator = Paginator(address,per_page=20)
    try:
        num = int(num)
        pages = paginator.page(num)
    except:
        pages = paginator.page(1)
    return render(request,'admin_app/main/dzlist.html',{'pages':pages})

def incrementaddress(request):
    '''增加地址'''
    print('this is increment address')
    #查询所有用户
    users = User.objects.all()
    return render(request,'admin_app/main/incrementaddress.html',{'users':users})

def incrementaddress_logic(request):
    '''增加地址逻辑'''
    print('this is increment address logic')
    #接收form表单信息
    consignee = request.POST.get('consignee')
    detailAddress = request.POST.get('detailAddress')
    postalcode = request.POST.get('postalcode')
    mobilephone = request.POST.get('mobilephone')
    telephone = request.POST.get('telephone')
    userid = request.POST.get('userid')
    print(consignee,detailAddress,postalcode,mobilephone,telephone,userid)
    #查询用户
    uid = int(userid)
    user = User.objects.get(pk=uid)
    try:
        with transaction.atomic():
            newAddress = Address(consignee=consignee,detailAddress=detailAddress,postalcode=postalcode,mobilephone=mobilephone,telephone=telephone,userid=user)
            newAddress.save()
    except:
        traceback.print_exc()
    return redirect('adm:adrslt')

def deladdress(request):
    '''删除地址'''
    print('this is delete address logic')
    #获取地址id
    aid = request.GET.get('aid')
    print(aid,type(aid))
    #查询并删除
    with transaction.atomic():
        aid = int(aid)
        address = Address.objects.get(pk=aid)
        address.delete()
    return HttpResponse(1)

def secondcategory(request):
    '''查询商品二级分类'''
    print('this is select second category')
    #获取一级分类id
    caid = request.GET.get('caid')
    if caid:
        caid = int(caid)
    #查询一级分类下的所有二级分类
        secondcategory=Menus.objects.filter(parent=caid)
        print(type(secondcategory),secondcategory)
        def mydefault(a):
            if isinstance(a,QuerySet):
                c=[]
                for i in a:
                    c.append(i)
                a=c
            if isinstance(a,Menus):
                a = {'id':a.id,'name':a.name,'parent':a.parent}
            return a
        #返回所有二级分类
        return JsonResponse({'sec':secondcategory},json_dumps_params={'default':mydefault})