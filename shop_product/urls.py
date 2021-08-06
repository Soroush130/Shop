from django.urls import path
from shop_product import views

urlpatterns = [
    path('', views.product_list),
    # path('', views.product_list.as_view()),
    path('product_detail/<int:product_id>', views.product_detail),
    path('category_product/<str:slug>', views.category_product),
    path('brand_category_product/<str:slug>', views.brand_category_product),
    path('filter_price', views.filter_price_product),
    path('<int:id>', views.product_comment),
    path('favourite/<int:id>', views.favourite_product),
    path('search/', views.search_header)
]
