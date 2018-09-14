import trace
import traceback

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
#在car.Py中创建购物车模板1，（购物车项：(book，amount，delete状态=0)，total_price,save_price,add方法，modify方法，delete方法）
#添加购物车物品
from order_app.car import Car
from order_app.models import TUadress, TOrder, OrderMiddle
from user_app.models import TUser


def addCar(request):
    #请求场景：1，bookdetail加入购物车,购物车页面改变数量失去焦点（携带加入数量）（（异步））2，购物车页面点击‘+’，点击其他加入购物车按钮，（异步）
    #接收参数：获取添加bookid,amount;
    book_id=int(request.GET.get('book_id'))
    amount=request.GET.get('amount')
    amount=(amount if amount else 1)
    flag=request.GET.get('flag')
    #获取购物车；
    car = request.session.get('car')

    #添加购物车：1，判断是否有购物车，没有购物车创建购物车对象，调用购物车add方法，添加购物车（bookid,amount）并保存到session中2，有购物车，直接调用add方法；
    try:
        if not car:
            car=Car()
            request.session['car'] = car
            car.addCar(book_id=int(book_id),amount=int(amount))
        else:
            if flag:
                car.modifyCar(book_id=int(book_id), amount=int(amount))
            else:
                print(99999)
                car.addCar(book_id=int(book_id), amount=int(amount))
        #返回响应，1，表示添加，0，表示添加失败：
        request.session['car'] = car
        for i in car.carItems:
            print(i.delete_status)
        car_item=car.get_car_item(book_id)
        item_price=car_item.amount*car_item.book.dang_price
        print(car.get_total_price())
        return JsonResponse({'total_price':car.get_total_price(),'save_price':car.get_save_price(),'item_price':item_price})
    except:
        traceback.print_exc()
        return HttpResponse('0')
# 购物车页面：
def car_page(request):
    #需求场景：1，点击每个页面购物车超链接：2，购物页面回复按钮（flag=1&book_id）：3，(flag=2&book_id)购物车删除按钮()；
    #从session中获取购物车
    car=request.session.get('car')
    amount=request.GET.get('amount')
    #判断是否存在购物车：1,没有，创建空购物车：
    if not car:
        car=Car()
        request.session['car']=car
    #获取参数(flag,book_id)
    flag=request.GET.get('flag')
    # 判断是否是回复请求还是删除请求,flag=1:调用购物车modify方法，flag=2，调用购物车delet_car方法；
    if flag=='1':
        book_id = request.GET.get('book_id')
        car.recoverCar(book_id=int(book_id))
    elif flag=='2':
        book_id = request.GET.get('book_id')
        car.deleteCar(book_id=int(book_id))
    elif flag=='3':
        book_ids=request.GET.getlist("book_id")
        print(book_ids)
        for i in book_ids:
            car.deleteCar(book_id=int(i))
    #将购物车对象传入模板中遍历；
    request.session['car']=car
    #通过用户查询其地址：
    for i in car.carItems:
        print(i.delete_status)
    user_name=request.session.get('user_name')
    t_address=TUadress.objects.filter(user__user_name=user_name)
    return render(request,'order_app/car.html',{'car':car,'t_address':t_address})
#模。判断购物车项的deleted状态为1，显示在恢复栏中；为0显示在购物车中：|\
#第三遍：
#地址页面：
# def adress_page(request):
#     #请求场景：1，注册和登陆直接跳转，2结算按钮跳转查询，3订单详情页直接购买（flag==1,book-id，amount，加入购物车，），4，放回购物车按钮（携带参数flag=2,book_id,添加购物车order——status：）：
#     #获取请求参数：
#     flag=request.GET.get('flag')
#     car=(request.session.get('car') if request.session.get('car') else Car())
#     book_id=request.GET.get('book_id')
#     amount=request.GET.get('amount')
#     user_name=request.session.get('user_name')
#     #判断flag：
#     if flag=='1':
#         car.addCar(book_id=book_id,amount=amount)
#         request.session['car']=car
#     elif flag=='2':
#         car.deleteCar_order(book_id=book_id)
#     #地址；
#     t_adress=TUadress.objects.filter(user__user_name=user_name)
#     default_adress=TUadress.objects.filter(user__user_name=user_name,default=1)
#     return render(request,'order_app/indent_3.html',{'t_adress':t_adress,'car':car,'default_adress':default_adress})
# #查询相应地址对象：
# def adress(request):
#     #请求场景：异步：
#     #接收参数：
#     name=request.POST.get('name')
#     t_adress1=TUadress.objects.filter(name=name)
#     def mydefault(o):
#         return list(o.values())
#     return JsonResponse(t_adress1,safe=False,json_dumps_params={'default':mydefault})
#
#
#
#
#
































def adress_page(request):
    #请求场景：1，car_page提交订单（携带当前地址的name）：2,在detail_page直接购买按钮{携带flag= 1标志，book_id,amount,从新添加物车}
    #获取请求参数
    flag=request.GET.get('flag')
    book_id = request.GET.get('book_id')
    amount = request.GET.get('amount')
    car = request.session.get('car')
    user_name=request.session.get('user_name')

    t_adress=TUadress.objects.filter(default=1,user__user_name=user_name)
    if flag=='1':
        if not car:
            car=Car()
        car.addCar(book_id=int(book_id),amount=int(amount))
        request.session['car']=car
    elif not flag:
        name=request.GET.get('name')
        t_adress = TUadress.objects.filter(name=name)
    return render(request,'order_app/indent.html',{'t_adress':t_adress,'car':car})
def order_ok_page(request):
    #请求场景：1个：持久化地址表单，订单表，中间项表
    #获取地址表单数据：
    id=request.POST.get('id')
    name = request.POST.get('name')
    user_name=request.session.get('user_name')
    user=TUser.objects.get(user_name=user_name)
    country = request.POST.get('country')
    city = request.POST.get('city')
    district = request.POST.get('district')
    address = request.POST.get('address')
    postecode = request.POST.get('postecode')
    telephone = request.POST.get('telephone')
    phone_num = request.POST.get('phone_num')
    default = request.POST.get('isdefault')
    print(country)
    if default:
        t_adress = TUadress.objects.filter(default=1)
        if t_adress:
            t_adress[0].default = None
            t_adress[0].save()
    #存储新地址：
    if not id:
        t_adress1=TUadress(user=user,name=name,country=country,city=city,default=default,district=district,address=address,postecode=postecode,phone_num=phone_num,telephone=telephone)
        t_adress1.save()
    else:
        t_adress1=TUadress.objects.get(id=id)
        t_adress1.user = user
        t_adress1.name= name
        t_adress1.country = country
        t_adress1.city = city
        t_adress1.default = default
        t_adress1.district = district
        t_adress1.address = address
        t_adress1.postcode = postecode
        t_adress1.phone_num = phone_num
        t_adress1.telephone = telephone
        t_adress1.save()
    #存储订单；
    car=request.session.get('car')
    t_order=TOrder(total_price=car.get_total_price(),order_addr=t_adress1,user=user)
    t_order.save()
    #中间表：
    for i in car.carItems:
        if not i.delete_status:
            i.book.sale_num+=i.amount
            i.book.save()
            OrderMiddle(object_count=i.amount,book=i.book,order=t_order,small_price=i.amount*i.book.dang_price).save()
    request.session['car']=""
    return render(request,'order_app/indent ok.html',{'t_order':t_order})








#
#
#
#
#
#
#
#
#
#
#
#
#







































#地址页面
# def adress_page(request):
#     #需求场景：1，强制登陆/后的注册 自动跳转到页面，2，点击结算 跳转到地址页面3，detail_page立即购买标签,4点击放回购物车：
#     #接收参数：
#     flag=request.GET.get('flag')
#     amount=request.GET.get('amount')
#     book_id=request.GET.get('book_id')
#     # 从session中获取用户名
#     user_name = request.session.get('user_name')
#     #从session中获取购物车：
#     car= request.session.get('car')
#     #判断是否有car:
#     if not car:
#         car=Car()
#     #判断flag：存在：car.addcar:持久化到session中；
#     if flag=='1':
#         car.addCar(book_id=int(book_id),amount=int(amount))
#     elif flag=='2':
#         #调用相关方法；
#         car.deleteCar_order(int(book_id))
#     request.session['car']=car
#     #通过用户名查询adress表；
#     adresses=TUadress.objects.filter(user__user_name=user_name)
#     #传值{address，car}
#     return render(request,'order_app/indent.html',{'addresses':adresses,'car':car})
# #提交订单：
# def order_ok_page(request):
#     #请求场景：adress_page提交按钮；
#     #获取参数：判断id 为’new‘:获取新建dress参数；
#     id=request.POST.get('id')
#     if id=='new':
#         user_name=request.POST.get('user_name')
#         pre_adress=request.POST.getlist('pre_adress')
#         address=request.POST.get('address')
#         postcode=request.POST.get('postcode')
#         telephone=request.POST.get('telephone')
#         phone_num=request.POST.get('phone_num')
#     # user_name,pre_adress(getlist),address,postcode,telephone,phone_num
#     #拼接pre_adress,address为address
#         address=''.join(pre_adress)+address
#     #通过user_name查询出user对象
#         user=TUser.objects.get(user_name=user_name)
#     #保存adress到TUadress中；
#         t_adress=TUadress(user=user,address=address,postecode=postcode,telephone=telephone,phone_num=phone_num)
#         t_adress.save()
#     #id不为new:获取adress参数user_name,address,# postcode,telephone,phone_num
#     else:
#         user_name = request.POST.get('user_name')
#         address = request.POST.get('address')
#         postcode = request.POST.get('postcode')
#         telephone = request.POST.get('telephone')
#         phone_num = request.POST.get('phone_num')
#
#     #通过user_name查询出user对象
#         user = TUser.objects.get(user_name=user_name)
#     #通过id找打adress对象,跟新adress对象
#         t_adress=TUadress.objects.get(pk=id)
#         t_adress.user=user
#         t_adress.address=address
#         t_adress.postecode=postcode
#         t_adress.telephone=telephone
#         t_adress.phone_num=phone_num
#         t_adress.save()
#     #---------------------------------------
#     #持久化订单中间表和订单表
#     #创建订单对象：
#     # 获取从session中购物车对象car.total_price_order
#     car=request.session.get('car')
#     #获取对应地址对象:使用啊adress对象：
#     #报存到order数据库中：
#     t_order=TOrder(total_price=car.get_total_price_order(),order_addr=t_adress,user=user)
#     t_order.save()
#     #创建订单中间表对象：
#     #遍历上面的给购物车对象car.items:for循环中创建中间表对象，并save
#     for i in car.carItems:
#         OrderMiddle(book=i.book,order=t_order,object_count=i.amount,small_price=i.amount*i.book.dang_price).save()
#     #return indent ok.html并将订单传入模板中
#     return render(request,'order_app/indent ok.html',{'id':t_order.id})