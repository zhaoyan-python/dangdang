from django.urls import path, include

from category_admin import views

urlpatterns = [
    path('cate_list/', views.cate_list, name='cate_list'),
    path('add_cate1/', views.add_cate1, name='add_cate1'),
    path('add_cate2/', views.add_cate2, name='add_cate2'),
    path('add_cate1_logic/',views.add_cate1_logic,name='add_cate1_logic'),
    path('add_cate2_logic/',views.add_cate2_logic,name='add_cate2_logic'),
    path('del_cate/',views.del_cate,name='del_cate'),
    path('reset_cate2_logic/', views.add_cate2_logic, name='reset_cate2_logic'),
    path('reset_cate1_logic/', views.add_cate1_logic, name='reset_cate1_logic'),
]