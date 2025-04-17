from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('books/', views.book_list, name='book_list'),
    path('books/manage/', views.book_manage, name='book_manage'),
    path('books/issue/', views.book_issue, name='book_issue'),
    path('books/return/<int:transaction_id>/', views.book_return, name='book_return'),
    path('fine/payment/<int:transaction_id>/', views.fine_payment, name='fine_payment'),
    path('membership/manage/', views.membership_manage, name='membership_manage'),
]