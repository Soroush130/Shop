from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ShopingDjango import views

urlpatterns = [
    path('account/', include("shop_account.urls")),
    path('products/', include("shop_product.urls")),
    path('cart/', include("shop_cart.urls")),
    path('contact/', include("shop_contact.urls")),
    path('blog/', include("shop_blog.urls")),
    path('todo/', include("shop_todo.urls")),
    path('admin/', admin.site.urls),
    path('', views.home_page),
    path('404', views.notfound_page),
    path('header', views.header, name="header"),
    path('footer', views.footer, name="footer"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
