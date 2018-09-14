from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from index_app.models import Category, TBook


def main_page(request):
    #一级分类queryset:
    cate1=Category.objects.filter(parent_id__isnull=True)
    #书queryset:
    books=TBook.objects.all()
    #查询前2个编辑推荐书籍：
    books_editor_recommend=books.order_by('-customer_score')[:10]
    #查询前10热销书：
    books_sale_hot=books.order_by('-sale_num')[:10]
    #查询前8新书：
    books_new_publish=books.order_by('-sale_time')[:8]
    #按照销量排序前30新书：
    books_new_sale=books.order_by('-sale_num','-sale_time')[:10]
    #所有的二级类：
    cates2=Category.objects.filter(parent_id__isnull=False)
    return render(request,'index_app/index.html',{'cate1':cate1,
                                                  'books_editor_recommend':books_editor_recommend,
                                                  'books_sale_hot':books_sale_hot,
                                                  'books_new_publish':books_new_publish,
                                                  'books_new_sale':books_new_sale,
                                                  'cates2':cates2,
                                                  'ranges': range(3)})
def bookdetails_page(request):
    #接收参数：
    id=request.GET.get('id')
    #查询相关书籍：
    print(id)
    book=TBook.objects.get(pk=id)
    return render(request,'index_app/Book details.html',{'book':book})
def book_list_page(request):
    #接收参数：
    #类别参数：
    category_name=request.GET.get('category_name')
    b_class=request.GET.get('b_class')
    #排序方式：
    order_cate=request.GET.get('order_cate')
    # 获取页码：
    num = request.GET.get('num')
    #查询书对象：
    if b_class=='1':
        #一级类别对象：
        cate1=Category.objects.get(category_name=category_name)
        #二级类别对象对应的书对象的id list
        # books_id_list=[j.id for i in cate1.category_set.all() for j in i.tbook_set.all()]
        #查询在这个范围类的书的queryset;
        # books=TBook.objects.filter(id__in=books_id_list)
        #二级列表对象的名字列表
        cate2_name_list=[i.category_name for i in cate1.category_set.all() ]
        #通过二级对象的名字列表查询书对象的queryset
        books= TBook.objects.filter(cate__category_name__in=cate2_name_list)
    elif b_class=='2':
        #查询二级分类对象：
        cate1=Category.objects.get(category__category_name=category_name)
        #查询书对象的queryset;
        books=TBook.objects.filter(cate__category_name= category_name)
        print(books)
    else:
        #查询所有
        cate1=None
        books = TBook.objects.all()
    #排序：
    if order_cate=='0':
        books=books.order_by('sale_num')
    elif order_cate=='1':
        books=books.order_by('dang_price')
    elif order_cate=='2':
        books=books.order_by('print_date')
    else:
        pass
    #书的数量：
    total_count=books.aggregate(mm=Count('id')).get('mm')
    #分页
    paginator = Paginator(books, per_page=3)
    num=(num if num else 1)
    page=paginator.page(num)
    #所有一级分类
    cates1=Category.objects.filter(parent_id__isnull=True)
    return render(request,'index_app/booklist.html',{'page':page,
                                                     'cates1':cates1,
                                                     'cate1':cate1,
                                                     'order_cate':order_cate,
                                                     'category_name':category_name,
                                                     'b_class':b_class,
                                                     'total_count':total_count})


