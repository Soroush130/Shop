from django.urls import path

from shop_todo import views

urlpatterns = [
    path('add-todo', views.add_todo),
    path('remove-todo/<int:id>', views.remove_todo)
]