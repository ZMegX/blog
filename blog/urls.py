# blog/urls.py

from django.urls import path, include
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, # Import here
    PostUpdateView, # Imported the PostUpdateView we have just created
    PostDeleteView,    
    CommentDeleteView,
    MyPostsView,
    
)
from .import views

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog_index'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),  
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),    
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/', MyPostsView.as_view(), name='my_posts'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]