from django.urls import path

from .posts_views import (
    CommentOnPostView,
    CreatePostView,
    DeleteCommentView,
    LikeCommentView,
    LikePostView,
    PostDetailView,
    ReplyCommentView,
)
from .views import FeedView

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create-post', CreatePostView.as_view(), name='create-post'),
    path('like-post', LikePostView.as_view(), name='like-post'),
    path('comment-on-post', CommentOnPostView.as_view(), name='comment-on-post'),
    path('like-comment', LikeCommentView.as_view(), name='like-comment'),
    path('reply-comment', ReplyCommentView.as_view(), name='reply-comment'),
    path('delete-comment', DeleteCommentView.as_view(), name='delete-comment'),
    path('<slug:slug>', PostDetailView.as_view(), name='post-detail'),
]
