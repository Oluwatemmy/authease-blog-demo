from django.urls import path
from . import frontend_views

urlpatterns = [
    path('', frontend_views.home, name='home'),
    path('post/<int:pk>/', frontend_views.post_detail, name='post-detail-view'),
    path('post/new/', frontend_views.create_post, name='create-post'),
    path('post/<int:pk>/edit/', frontend_views.edit_post, name='edit-post'),
    path('post/<int:pk>/delete/', frontend_views.delete_post, name='delete-post'),
    path('post/<int:pk>/like/', frontend_views.like_post, name='like-post'),
    path('post/<int:pk>/comment/', frontend_views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', frontend_views.delete_comment, name='delete-comment'),
    path('my-posts/', frontend_views.my_posts, name='my-posts-view'),
]
