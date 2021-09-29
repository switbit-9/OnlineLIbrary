
from collections import namedtuple
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout', views.logout , name='logout'),
    path('profile/', views.profile, name='profile'),
    path('borrow/<int:id>', views.borrow, name='borrow'),
    path('unborrow/<int:id>', views.unborrow, name='unborrow'),
    path('addbook', views.Addbook.as_view(), name='addbook'),
    path('books', views.books, name='books'),
    path('authors', views.authors, name='authors'),
    path('author/<int:id>', views.author, name='author'),
    path('prove/', views.prove, name='prove'),
    path('search/', views.search, name='search'),
    path('save/<int:id>', views.save, name='save'),
    path('unsave/<int:id>', views.unsave, name='unsave'),
    path('saved/', views.saved, name='saved'),
    path('book/<int:id>', views.book, name='book'),
    path('settings', views.settings, name='settings'),
    path('settings/edit', views.EditView.as_view(), name='edit'),
    path('settings/delete', views.delete, name='delete'), 
    path('admin/', views.admin, name='admin'),
    path('manage/books', views.manage_books, name='manageb'),
    path('manage/books/delete/<int:id>', views.delete_book, name='deletebook'),
    path('manage/users', views.manage_user, name='manageu'),
    path('manage/users/delete/<int:id>', views.delete_user, name='deleteuser'),
    path('manage/books/archive/<int:id>', views.archive, name='archive'),
    path('manage/archive', views.archived_books, name='archived'),
    path('manage/archive/delete/<int:id>', views.unarchive, name='unarchived'),
    path('manage/activity', views.allactivity, name='allactivity'),
    path('manage/issued', views.issued, name='issued')
]
