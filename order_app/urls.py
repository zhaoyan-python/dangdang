
from django.urls import path, include

from order_app import views

urlpatterns = [
   path('adress_page/',views.adress_page,name='adress_page'),
   path('add_car/',views.addCar,name='add_car'),
   path('car_page/',views.car_page,name='car_page'),
   path('order_ok_page/',views.order_ok_page,name='order_ok_page'),
]

