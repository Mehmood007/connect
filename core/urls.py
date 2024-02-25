from django.urls import path

from .posts_views import CreatePostView
from .views import FeedView

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create-post', CreatePostView.as_view(), name='create-post'),
]
