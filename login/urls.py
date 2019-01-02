from django.urls import path, include
from login import views
urlpatterns = [
    path('main/',views.login,name='login'),
    path('main/logic/',views.login_logic,name='logic'),
    path('main/logic/re/',views.reemail,name='re'),
    path('main/logout/',views.logout,name='out'),
]