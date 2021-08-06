from django.urls import path

from shop_blog import views

urlpatterns = [
    path('blog-list', views.blog_list),
    path('blog-detail/<int:id>', views.blog_detail),
    path('rate/<int:id>', views.rate_blog),
    path('comment/<int:id>', views.comment_product),
    path('reply_comment/<int:blog_id>/<int:comment_id>', views.reply_comment_product)
]