import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect


# Create your views here.
from index_app.models import Category


def cate_list(request):
    #需求场景：1，主页按钮(分页),点击页码（num，下一页，上一页(num)
    #获取参数：
    num=request.GET.get('num')
    num=(num if num else 1)
    #查询所有类别：
    cates=Category.objects.all()
    #分页：
    paginator=Paginator(cates,per_page=3)
    page=paginator.page(num)
    return render(request,'obj_admin/main/categories/splb.html',{'page':page})
def add_cate1(request):
    #跟新按钮：
    #获取提交数据：
    cate_id=request.GET.get('id')
    category_name=request.session.get('category_name')
    cate=Category.objects.filter(id=cate_id)
    #清楚session数据：
    request.session['category_name']=''
    return render(request,'obj_admin/main/categories/zjsp.html',{'category_name':category_name,'cate':cate})
def add_cate2(request):
    #请求场景：1.点击主页面：2，add_cate2_logic 重定向：：
    cate_id = request.GET.get('id')
    cate = Category.objects.filter(id=cate_id)
    #查询所有cate1，
    cate1=Category.objects.filter(parent_id__isnull=True)
    #跳转，传值，渲染
    category_name = request.session.get('category_name')
    # 清楚session数据：
    request.session['category_name']=''
    return render(request,'obj_admin/main/categories/zjzlb.html',{'cate1':cate1,'category_name':category_name,'cate':cate})
def add_cate1_logic(request):
    #请求场景：1，父类别提交按钮：
    #获取请求参数：category_name
    id=request.GET.get('id')
    category_name=request.GET.get('category_name')
    #添加父类别：
    try:
        with transaction.atomic():
            request.session['category_name'] = category_name
            if id:
                Category.objects.filter(pk=id).update( category_name= category_name)
            else:
                request.session['category_name']=category_name
                Category(category_name=category_name).save()
    except:
        traceback.print_exc()
    #从定性到当前页面（add_cate1）
    return redirect('category_admin:add_cate1')
def reset_cate1_logic(request):
    category_name = request.GET.get('category_name')
    try:
        with transaction.atomic():
            Category.objects.filter(category_name=category_name).delete()
    except:
        traceback.print_exc()
    return redirect('category_admin:add_cate1')
def add_cate2_logic(request):
    #需求场景：提交，重置按钮
    #获取参数：
    print(2131313)
    id = request.GET.get('id')
    cate1_category_name=request.GET.get('cate1_category_name')
    cate2_category_name=request.GET.get('cate2_category_name')
    #查询父类对象：
    cate1=Category.objects.filter(category_name=cate1_category_name)[0]

    try:
        request.session['category_name'] = cate2_category_name
        with transaction.atomic():
            #添加查特cate2:
            if id:
                Category.objects.filter(pk=id).update( category_name= cate2_category_name,parent_id=cate1)
            else:
                Category(category_name=cate2_category_name,parent_id=cate1).save()
    except:
        traceback.print_exc()
        print(2131231)
    return redirect('category_admin:add_cate2')
def reset_cate2_logic(request):
    category_name = request.GET.get('category_name')
    try:
        with transaction.atomic():
            Category.objects.filter(category_name=category_name).delete()
    except:
        traceback.print_exc()
    return redirect('category_admin:add_cate2')
def del_cate(request):
    #请求场景：删除按钮：
    #获取参数：getlist
    books_id=request.GET.getlist('books_id')
    #删除：
    for i in books_id:
        cate=Category.objects.get(pk=i)
        cate.t_delete=1
        cate.save()
    return redirect('category_admin:cate_list')




