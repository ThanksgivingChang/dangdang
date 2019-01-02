from django.urls import path, include
from indent import views

urlpatterns = [
    path('main/',views.getindent,name='get'),
    path('main/ok/',views.retindent,name='ret'),
    path('main/logic/',views.indent_logic,name='logic'),
    path('main/set/address/',views.setaddress,name='set'),
    path('main/backto/cart/',views.backToCart,name='back')

]