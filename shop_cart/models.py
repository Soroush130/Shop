from django.db import models

from django import forms
from shop_account.models import UserAccount
from shop_product.models import Product


# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.user.name


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class Order(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True)
    # فیلد زیر برای زمانی که کاربر سبد خرید پرداخت میکنه
    create = models.DateTimeField(blank=True, null=True)
    email = models.EmailField()
    f_name = models.CharField(max_length=300)
    l_name = models.CharField(max_length=300)
    phone = models.IntegerField(default=None)
    address = models.CharField(max_length=700)
    address_2 = models.CharField(max_length=700, default=None)
    # فیلد زیر برای زمانی که خود سفارش ایجاد میشه
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order')
    quantity = models.IntegerField()

    def total_price(self):
        return 1

    def __str__(self):
        return self.user.name


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'f_name', 'l_name', 'phone', 'address', 'address_2']


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.IntegerField()

    def __str__(self):
        return self.code


class CouponForm(forms.Form):
    code = forms.CharField()
