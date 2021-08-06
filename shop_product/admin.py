from django.contrib import admin

from shop_product.models import Product, Brand, Gallery, Category, Comment, Chart, Slider


# Register your models here.

class CategoryInline(admin.StackedInline):
    model = Category


class GalleryInline(admin.StackedInline):
    model = Gallery


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'count', 'discount']
    search_fields = ['title']
    # list_editable = ['title']
    inlines = [GalleryInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Gallery)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Chart)
admin.site.register(Slider)
