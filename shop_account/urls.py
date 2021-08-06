from django.contrib import admin
from django.urls import path, include

from shop_account import views

urlpatterns = [
    path('header_profile', views.header_profile, name="header_profile"),
    path('footer_profile', views.footer_profile, name="footer_profile"),
    path('login', views.login_page),
    path('register', views.register_page),
    path('log-out', views.log_out),
    path('profile', views.user_profile),
    path('update', views.update_profile),
    path('change-password', views.change_password),
    path('favourite-list', views.favourite_list),
    path('order-history', views.order_history),
    path('product-list', views.product_list),
    path('search-product', views.search_list_product),
    path('user-list', views.user_list),
    path('search-user', views.search_list_user),
    path('contact', views.contact)
]
