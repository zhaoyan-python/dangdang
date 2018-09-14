

from django.urls import path, include

from adress_admin import views

urlpatterns = [
    path('adress_list/',views.adress_list,name='adress_list'),
    path('add_adress/',include(([path('add_adress_logic',views.add_adress_logic,name='add_adress_logic'),
                                 path('add_adress_page',views.add_adress_page,name='add_adress_page')],'add_adress'))),
    path('del_adress_logic/',views.del_adress_logic,name='del_adress_logic')
]
