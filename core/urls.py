from django.urls import path

from .messenger_views import InboxDetailView, InboxView
from .posts_views import (
    CommentOnPostView,
    CreatePostView,
    DeleteCommentView,
    LikeCommentView,
    LikePostView,
    PostDetailView,
    ReplyCommentView,
)
from .views import (
    AcceptFriendRequestView,
    BlockUserView,
    FeedView,
    FriendRequestView,
    RejectFriendRequestView,
    UnfriendRequestView,
)

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create-post', CreatePostView.as_view(), name='create-post'),
    path('like-post', LikePostView.as_view(), name='like-post'),
    path('comment-on-post', CommentOnPostView.as_view(), name='comment-on-post'),
    path('like-comment', LikeCommentView.as_view(), name='like-comment'),
    path('reply-comment', ReplyCommentView.as_view(), name='reply-comment'),
    path('delete-comment', DeleteCommentView.as_view(), name='delete-comment'),
    path('core/inbox', InboxView.as_view(), name='inbox'),
    path('core/inbox/<username>', InboxDetailView.as_view(), name='chat-box'),
    path('friend-request/<id>', FriendRequestView.as_view(), name='friend-request'),
    path(
        'accept-friend-request',
        AcceptFriendRequestView.as_view(),
        name='accept-friend-request',
    ),
    path(
        'reject-friend-request',
        RejectFriendRequestView.as_view(),
        name='reject-friend-request',
    ),
    path(
        'unfriend',
        UnfriendRequestView.as_view(),
        name='unfriend',
    ),
    path('core/block-user', BlockUserView.as_view(), name='block-user'),
    path('<slug:slug>', PostDetailView.as_view(), name='post-detail'),
]
