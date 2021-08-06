from django.contrib import admin

# Register your models here.
from shop_cart.models import Cart, Order, ItemOrder, Coupon


# class CouponAdmin(admin.ModelAdmin):
#     list_display = ['code', 'active', 'discount', 'start', 'end']
#
#
# admin.site.register(Cart)
# admin.site.register(Order)
# admin.site.register(ItemOrder)
# admin.site.register(Coupon, CouponAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user', 'product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'f_name', 'l_name', 'address', 'address_2', 'create', 'paid']
    inlines = [ItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon)
