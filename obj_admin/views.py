import traceback
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os.path

from index_app.models import TBook, Category


def get_fliename(name):
    ext=os.path.splitext(name)[1]
    u=str(uuid.uuid4())
    return u+ext
# Create your views here.
#商品管理总页面
def main_page(request):
    #需求场景：首页我的当当
    return render(request,'obj_admin/index.html')

def add_book_page(request):
    #跟新按钮，book_id
    #获取请求参数：
    book_id=request.GET.get('book_id')
    book=TBook.objects.filter(id=book_id)
    cates2=Category.objects.filter(parent_id__isnull=False)
    return render(request,'obj_admin/main/book-add-delete-update-list/add.html',{'cates2':cates2,'book':book})

def book_list(request):
    #需求场景：点击商品列表按钮第一次过来，2，点击页码，和下一页，上一页，携带num页号；3,点击删除按钮携带（num,book_id,flag=1），4

    #接收参数：
    flag=request.GET.get('flag')
    num=request.GET.get('num')
    num=(num if num else 1)
    books_id=request.GET.getlist('books_id')
    if flag=='1':
        for i in books_id:
            book=TBook.objects.get(id=i)
            book.t_delete=1
            book.save()
    books=TBook.objects.all()
    paginator=Paginator(books,per_page=3)
    page=paginator.page(num)
    return render(request,'obj_admin/main/book-add-delete-update-list/list.html',{'page':page})



def add_book(request):
    book_id=request.POST.get('book_id')
    book_total_count=request.POST.get('book_total_count')
    book_name=request.POST.get('book_name')
    author_name = request.POST.get('author_name')
    publish_firm = request.POST.get('publish_firm')
    cate2 = request.POST.get('cate2')
    publishing_date = request.POST.get('publishing_date')
    print_date = request.POST.get('print_date')
    print_num = request.POST.get('print_num')
    isbn= request.POST.get('isbn')
    font_num = request.POST.get('font_num')
    page_num = request.POST.get('page_num')
    kaiben = request.POST.get('kaiben')
    paper = request.POST.get('paper')
    pack = request.POST.get('pack')
    price = request.POST.get('price')
    dang_price = request.POST.get('dang_price')
    editor_recommend = request.POST.get('editor_recommend')
    content_intro = request.POST.get('content_intro')
    author_intro = request.POST.get('author_intro')
    catalogue = request.POST.get('catalogue')
    media_comments = request.POST.get('media_comments')
    excerpt = request.POST.get('excerpt')
    # t_delete = request.POST.get('t_delete')
    # blank = request.POST.get('blank')
    # sale_num = request.POST.get('sale_num')
    # sale_time = request.POST.get('sale_time')
    customer_score = request.POST.get('customer_score')
    l_vrsion = request.POST.get('l_vrsion')
    comment_times = request.POST.get('comment_times')
    pic_url=request.FILES.get('pic_url')
    print(l_vrsion,comment_times,pic_url,cate2)
    cate2=Category.objects.filter(category_name=cate2)[0]
    try:
        with transaction.atomic():
            if not book_id:
                TBook(book_total_count=book_total_count,book_name=book_name,pic_url=pic_url,author_name=author_name,
                      publish_firm=publish_firm,cate=cate2,publishing_date=publishing_date,
                      print_date=print_date,print_num=print_num,isbn=isbn,font_num=font_num,
                      page_num=page_num,kaiben=kaiben,paper=paper,pack=pack,price=price,
                      dang_price=dang_price,editor_recommend=editor_recommend,
                      content_intro=content_intro,author_intro=author_intro,catalogue=catalogue,
                      media_comments=media_comments,excerpt=excerpt,
                      # t_delete=t_delete,blank=blank,
                      # sale_num=sale_num,sale_time=sale_time,
                      customer_score=customer_score,
                      l_vrsion=l_vrsion,comment_times=comment_times).save()
                return redirect('obj_admin:add_book_page')
            else:
                book = TBook.objects.get(pk=book_id)
                book.book_total_count = book_total_count
                book.book_name = book_name
                if pic_url:
                    pic_url.name = get_fliename(pic_url.name)
                    book.pic_url = pic_url
                book.author_name = author_name
                book.publish_firm = publish_firm
                book.cate = cate2
                book.publishing_date = publishing_date
                book.print_date = print_date
                book.print_num = print_num
                book.isbn = isbn
                book.font_num = font_num
                book.page_num = page_num
                book.kaiben = kaiben
                book.paper = paper
                book.pack = pack
                book.price = price
                book.dang_price = dang_price
                book.editor_recommend = editor_recommend
                book.content_intro = content_intro
                book.author_intro = author_intro
                book.catalogue = catalogue
                book.media_comments = media_comments
                book.excerpt = excerpt
                # t_delete=t_delete,blank=blank,
                # sale_num=sale_num,sale_time=sale_time,
                book.customer_score = customer_score
                book.l_vrsion = l_vrsion
                book.comment_times = comment_times
                book.save()
                return redirect('obj_admin:book_list')
    except:
        traceback.print_exc()
        return HttpResponse('服务器忙')
#






