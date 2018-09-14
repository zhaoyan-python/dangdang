import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from order_app.models import TUadress
from user_app.models import TUser


def adress_list(request):
    #请求分析：1，主页面，2，上一页，下一页，页码，3，散出，跟新，添加逻辑重定向：
    #接收参数：
    num=(request.GET.get('num') if request.GET.get('num') else 1)
    #查询所有：
    adresses=TUadress.objects.filter(t_del__isnull=True)
    #分页：
    paginator=Paginator(adresses,per_page=3)
    page=paginator.page(num)
    return render(request,'obj_admin/main/adress/dzlist.html',{"page":page})
def add_adress_page(request):
    #请求场景：添加按钮：
    #接收参数：
    return render(request,'obj_admin/main/adress/add_adress.html')
def add_adress_logic(request):
    #亲求场景：1，提交按钮;
    #获取参数：
    user_name=request.POST.get('user_name')
    user=TUser.objects.filter(user_name=user_name)[0]
    name=request.POST.get('name')
    telephone=request.POST.get('telephone')
    #保存：
    TUadress(user=user,name=name,telephone=telephone).save()
    return redirect("adress_admin:adress_list")
def del_adress_logic(request):
    #请求场景：略：
    #获取参数：getlist:
    ids=request.GET.getlist('id')
    try:
        with transaction.atomic():
            for i in ids:
                TUadress.objects.filter(pk=i).delete()
    except:
        traceback.print_exc()
    return redirect('adress_admin:adress_list')
adsadadasd


