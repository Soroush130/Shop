from django.urls import path
from shop_cart import views

urlpatterns = [
    path('<int:id>', views.add_cart),
    path('cart-detail', views.cart_detail),
    path('remove/<int:id>', views.remove_cart),
    path('order-detail/<int:order_id>', views.order_detail),
    path('create', views.order_create),
    path('coupon/<int:order_id>', views.coupon_order),

    path('add-single/<int:id>', views.add_single),
    path('remove-single/<int:id>', views.remove_single),
]
