
from django.urls import path

from index_app import views

urlpatterns = [
    path('main_page/',views.main_page,name='main_page'),
    path('bookdetails_page/',views.bookdetails_page,name='bookdetails_page'),
    path('book_list_page/',views.book_list_page,name='book_list_page'),
]
