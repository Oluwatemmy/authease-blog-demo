from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/me/', views.MyPostsView.as_view(), name='my-posts'),
    path('posts/<int:pk>/like/', views.LikeToggleView.as_view(), name='like-toggle'),
    path('comments/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
]
