from django.db import models

# Create your models here.
from index_app.models import TBook
from user_app.models import TUser


class OrderMiddle(models.Model):
    book= models.ForeignKey(to=TBook, on_delete=models.CASCADE)
    order= models.ForeignKey(to='TOrder',on_delete=models.CASCADE)
    object_count = models.IntegerField()
    small_price = models.IntegerField(null=True)
    class Meta:
        db_table = 'order_middle'
class TUadress(models.Model):
    create_time=models.DateTimeField(auto_now_add=True,null=True)
    user = models.ForeignKey(to=TUser,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    address = models.TextField(blank=True, null=True)
    postecode = models.CharField(max_length=10, null=True)
    phone_num = models.CharField(max_length=12, null=True)
    telephone = models.CharField(max_length=13, null=True)
    t_del = models.IntegerField(null=True)
    country=models.CharField(max_length=20,null=True)
    city=models.CharField(max_length=20,null=True)
    district=models.CharField(max_length=20,null=True)
    default=models.SmallIntegerField(null=True)
    blank = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = 't_uadress'
class TOrder(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    order_addr = models.ForeignKey(to=TUadress,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(to=TUser,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(null=True)
    class Meta:
        db_table = 't_order'


