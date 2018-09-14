# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
class Category(models.Model):
    category_name = models.CharField(max_length=20, null=True)
    parent_id = models.ForeignKey(to='self',null=True,on_delete=models.CASCADE)
    t_delete=models.SmallIntegerField()
    class Meta:
        db_table = 'category'
class TBook(models.Model):
    book_total_count=models.IntegerField(null=True)
    pic_url=models.ImageField(upload_to='pic',default="images/9269536-1_l_1.jpg")
    book_name=models.CharField(max_length=20,null=True)
    author_name = models.CharField(max_length=20,null=True)
    publish_firm = models.CharField(max_length=30,null=True)
    publishing_date = models.DateField(null=True)
    version = models.IntegerField(null=True)
    print_date = models.DateField(null=True)
    print_num = models.IntegerField(null=True)
    isbn = models.IntegerField(null=True)
    font_num = models.BigIntegerField(null=True)
    page_num = models.IntegerField(null=True)
    kaiben = models.IntegerField(null=True)
    paper = models.CharField(max_length=20,null=True)
    pack = models.CharField(max_length=10,null=True)
    price = models.IntegerField(null=True)
    dang_price = models.IntegerField(null=True)
    editor_recommend = models.TextField(null=True)
    content_intro = models.TextField(null=True)
    author_intro = models.TextField(null=True)
    catalogue = models.TextField(null=True)
    media_comments = models.TextField(null=True)
    excerpt = models.CharField(max_length=20,null=True)
    t_delete = models.IntegerField(null=True)
    blank = models.CharField(max_length=20,null=True)
    sale_num = models.IntegerField(default=0)
    sale_time = models.DateTimeField(null=True,auto_now_add=True)
    customer_score = models.IntegerField(null=True)
    l_vrsion = models.IntegerField(null=True)
    comment_times=models.IntegerField(null=True)
    cate = models.ForeignKey(to='Category', on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = 't_book'



