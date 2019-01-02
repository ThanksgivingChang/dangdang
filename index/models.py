from django.db import models

# Create your models here.
class Menus(models.Model):
    '''描述一本书的类别'''
    name = models.CharField(max_length=30)
    parent = models.IntegerField()
    class Meta:
        db_table = 'd_menus'

class Product(models.Model):
    '''描述一本书的静态属性'''
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True)
    face = models.ImageField(upload_to='media')
    publishing_house = models.CharField(max_length=100)
    edition = models.SmallIntegerField()
    publishing_time = models.DateTimeField()
    print_time = models.SmallIntegerField()
    isbn = models.CharField(max_length=50)
    word = models.IntegerField()
    number_of_page=models.IntegerField(db_column='page')
    format_of_book = models.CharField(max_length=30,db_column='format')
    paper_size = models.CharField(max_length=10)
    packaging = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    menus = models.ForeignKey(to=Menus,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'd_product'

class AddProduct(models.Model):
    '''描述一本书的动态属性'''
    sales = models.IntegerField()
    price = models.FloatField()
    dangdang_price = models.FloatField()
    score = models.FloatField(null=True)
    issue = models.DateTimeField()
    recommand = models.SmallIntegerField()
    product_id=models.OneToOneField(to=Product,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = 'd_addproduct'


