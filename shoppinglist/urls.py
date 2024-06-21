from . import views
from django.urls import path
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
]