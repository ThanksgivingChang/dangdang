from django.db import models
from login.models import User
from index.models import Product,AddProduct

# Create your models here.
class Address(models.Model):
    '''描述一个用户的地址'''
    consignee= models.CharField(max_length=50)
    detailAddress = models.CharField(max_length=200)
    postalcode = models.CharField(max_length=10)
    telephone = models.CharField(max_length=12,null=True)
    mobilephone = models.CharField(max_length=15,null=True)
    userid = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'd_address'

class Orders(models.Model):
    '''描述一个订单'''
    orderNumber = models.CharField(max_length=30)
    dateInProduct = models.DateTimeField()
    status = models.CharField(max_length=10)
    freight = models.FloatField()
    #总金额
    expenditure = models.FloatField(0)
    customer = models.ForeignKey(to=User,on_delete=models.SET_NULL,null=True)
    address = models.ForeignKey(to=Address,on_delete=models.SET_NULL,null = True)
    class Meta:
        db_table = 'd_orders'

class OrderItems(models.Model):
    '''描述一个订单项'''
    productName = models.CharField(max_length=100)
    price = models.FloatField()
    amount = models.IntegerField()
    subtotal = models.FloatField()
    orderid = models.ForeignKey(to=Orders,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = 'd_orderitems'



