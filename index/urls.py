from django.urls import path, include
from index import views

urlpatterns = [
    path('index/', views.dangdang, name='index'),
    path('main/bookdetails/', views.bookdetails, name='bkdl'),
    path('main/booklist/', views.booklist, name='bklt'),
    path('main/test/',views.booktest,name='bt'),

]