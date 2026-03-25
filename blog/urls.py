from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    # Line of code: Crucial interaction paths
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/liked-users/', views.get_liked_users, name='liked-users'),
    path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('comment/<int:pk>/hide/', views.hide_comment, name='hide-comment'),
]
