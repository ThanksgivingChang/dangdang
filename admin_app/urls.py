
from django.urls import path, include
from admin_app import views

urlpatterns = [
    path('main/',views.getadmin,name='main'),
    path('main/addproduct/',views.addproduct,name='add'),
    path('main/productlist/',views.productlist,name='prolist'),
    path('main/addproduct/parentcategory/',views.addparentcategory,name='addpc'),
    path('main/addproduct/soncategory/',views.addsoncategory,name='addsc'),
    path('main/categorylsit/',views.categorylsit,name='ctlt'),
    path('main/addresslist/',views.addresslist,name='adrslt'),
    path('main/addproduct/secategopry/',views.secondcategory,name='sec'),
    path('main/addproduct/logic/',views.addproduct_logic,name='add_logic'),
    path('main/subproduct/',views.subproduct,name='sub'),
    path('main/setproduct/',views.setproduct,name='set'),
    path('main/setproduct/logic/',views.setproduct_logic,name='set_logic'),
    path('main/addresslist/incrementaddress/',views.incrementaddress,name='inc'),
    path('main/addresslist/incrementaddress/logic',views.incrementaddress_logic,name='inc_logic'),
    path('main/addresslist/deladdress',views.deladdress,name='deladdress'),
    path('main/addprodcut/parentcategory/logic/',views.addparentcategory_logic,name='category_logic'),
    path('main/addprodcut/soncategory/logic/',views.addsoncategory_logic,name='soncategory_logic'),
    path('main/delcategory/',views.delcategory,name='delcate')

]
