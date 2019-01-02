from django.urls import path, include
from register import views
urlpatterns = [
    path('main/',views.register,name='register'),
    path('main/register/logic/',views.register_logic,name='logic'),
    path('main/register/checkemail',views.email_check,name='email'),
    path('main/register/checkemaillogic',views.email_checklogic,name='checkEmailLogic'),
    path('main/register/success/',views.register_success,name='suc'),
    path('main/register/re/',views.reemail,name='re'),
    path('main/register/pinsecurity/',views.pinSecurity,name='safe'),
    path('main/register/getcaptcha/',views.getcaptcha,name= 'captcha'),
    path('main/register/checkcaptcha/',views.checkCaptcha,name= 'check')
]