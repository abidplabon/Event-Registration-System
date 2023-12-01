from django.urls import path
from App_Posts import views
from .views import PostListAPIView, PostDetailAPIView, LikeListAPIView, LikeDetailAPIView


app_name = "App_Posts"

urlpatterns = [
    path("", views.home, name="home"),
    path("liked/<pk>/", views.liked, name="liked"),
    path("unliked/<pk>/", views.unliked, name="unliked"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('likes/', LikeListAPIView.as_view(), name='like-list'),
    path('likes/<int:pk>/', LikeDetailAPIView.as_view(), name='like-detail'),
]
