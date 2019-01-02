from django.urls import path, include
from cart import views
urlpatterns = [
    path('main/',views.mycart,name='mycart'),
    path('main/addproduct/',views.addproduct,name='add'),
    path('main/setCartItem/',views.setCartItemAmount,name='set'),
    path('main/delCartItem/',views.delCartItem,name='del'),
    path('main/trueDelCartItem/',views.trueDelCartItem,name='trueDel'),
    path('main/reCartItem/',views.reCartItem,name='re'),

]