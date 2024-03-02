from core.models import Comment, Notification, Post
from userauths.models import User

# Notifications Keys
noti_new_follower = 'New Follower'


def send_notification(
    user: User = None,
    sender: User = None,
    post: Post = None,
    comment: Comment = None,
    notification_type: str = None,
):
    notification = Notification.objects.create(
        user=user,
        sender=sender,
        post=post,
        comment=comment,
        notification_type=notification_type,
    )
    return notification
