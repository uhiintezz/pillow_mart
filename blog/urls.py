from django.urls import path
from .views import *


urlpatterns = [
    path('search/', Search.as_view(), name='search'),
    path('comment/<int:pk>/', CreateComment.as_view(), name='create_comment'),
    path('category/<slug:cat_slug>', PostByCategory.as_view(), name='post_category'),
    path('<slug:post_slug>/', PostDetailView.as_view(), name='post_single'),
    path('tag/<slug:tag_slug>', PostByTag.as_view(), name='post_tag'),
    path('',  PostListView.as_view(), name='post_list'),


]