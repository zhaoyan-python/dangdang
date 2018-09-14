"""dangdang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from obj_admin import views

urlpatterns = [
    path('main_page/',views.main_page,name='main_page'),
    path('add_book_page/',views.add_book_page,name='add_book_page'),
    path('book_list/',views.book_list,name='book_list'),
    path('add_book/',views.add_book,name='add_book'),
]
