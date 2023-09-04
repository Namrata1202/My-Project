# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('bookUser/', views.User_List, name='User-list'),
    path('loginUser/', views.custom_login, name='custom_login'),   
    path('mybook/', views.My_list, name='My_list')

]