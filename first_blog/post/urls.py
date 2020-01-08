from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    # path('detail/<int:pk>/', views.detail, name='detail'),
    path('create/', views.create_post, name='creat_post'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.delete, name='post_delete'),
]
