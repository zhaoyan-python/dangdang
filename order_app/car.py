#创建订单项类：
from index_app.models import TBook
class CarItem:
    def __init__(self,book_id,amount,delete_status=None):
        book=TBook.objects.get(pk=book_id)
        self.book=book
        self.amount=amount
        self.delete_status=delete_status

#创建购物车模板：
class Car:
    def __init__(self):
        self.carItems=[]
    def addCar(self,book_id,amount):
        for i in self.carItems:
            if i.book.id == book_id and not i.delete_status:
                print(i.delete_status)
                i.amount += amount
                print(123)
                return
        self.carItems.append(CarItem(book_id, amount))
    def recoverCar(self,book_id):
        count=0
        for i in self.carItems:
            if i.book.id==book_id:
                count+=i.amount
                self.carItems.remove(i)
        self.carItems.append(CarItem(book_id, count))
    def deleteCar(self,book_id):
        for i in self.carItems:
            if i.book.id == book_id :
                i.delete_status=1
    def modifyCar(self,book_id,amount=None):
        if not amount:
            for i in self.carItems:
                if i.book.id == book_id:
                    i.delete_status = None
        elif amount:
            for i in self.carItems:
                if i.book.id == book_id:
                    i.amount = amount
    def get_total_price(self):
        self.total_price=sum([i.book.dang_price*i.amount for i in self.carItems if not i.delete_status])
        return self.total_price
    def get_save_price(self):
        self.save_price=sum([i.book.price*i.amount for i in self.carItems if not i.delete_status])-self.total_price
        return self.save_price
    # def get_total_price_order(self):
    #     self.total_price_order = sum([i.book.dang_price * i.amount for i in self.carItems if not i.delete_status])
    #     return self.total_price_order
    def get_car_item(self,book_id):
        for i in self.carItems:
            if i.book.id == book_id:
                return i
