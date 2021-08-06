from django.contrib import admin

# Register your models here.
from shop_blog.models import Blog, RateBlog, Comment

admin.site.register(Blog)
admin.site.register(RateBlog)
admin.site.register(Comment)