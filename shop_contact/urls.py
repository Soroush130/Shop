from django.urls import path

from shop_contact import views

urlpatterns = [
    path('', views.contact_page),
    path('about-us', views.about_page)
]
