
from django.urls import path
from user_app import views

urlpatterns= [
    path('regist_page/',views.regist_page,name='regist_page'),
    path('regist_logic/',views.regist_logic,name='regist_logic'),
    path('name_check/',views.name_check,name='name_check'),
    path('get_captcha/',views.get_captcha,name='get_captcha'),
    path('check_captcha/',views.check_captcha,name='check_captcha'),
    path('regist_ok_page/',views.regist_ok_page,name='regist_ok_page'),
    path('login_page/',views.login_page,name='login_page'),
    path('login_logic/',views.login_logic,name='login_logic'),
    path('send_email/',views.send_email,name='send_email')
]
