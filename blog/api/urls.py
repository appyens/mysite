from django.urls import path
from blog.api import views

app_name = 'blog_api'

urlpatterns = [
    path('list/', views.PostListAPIView.as_view(), name='list'),
    path('<slug:slug>/', views.PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/update/', views.PostUpdateAPIView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.PostDeleteAPIView.as_view(), name='delete'),
    path('post/create/', views.PostCreateAPIView.as_view(), name='create'),
]