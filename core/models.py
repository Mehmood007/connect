from typing import Any, List

import shortuuid
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User, user_directory_path
from utils.base_model import BaseModel

VISIBILITY = (
    ('Only Me', 'Only Me'),
    ('Everyone', 'Everyone'),
)

FRIEND_REQUEST = (
    ('pending', 'pending'),
    ('accept', 'Accept'),
    ('reject', 'Reject'),
)


NOTIFICATION_TYPE = (
    ('Friend Request', 'Friend Request'),
    ('Friend Request Accepted', 'Friend Request Accepted'),
    ('New Follower', 'New Follower'),
    ('New Like', 'New Like'),
    ('New Comment', 'New Comment'),
    ('Comment Liked', 'Comment Liked'),
    ('Comment Replied', 'Comment Replied'),
)


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default='everyone', choices=VISIBILITY)
    pid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Post'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title) + '-' + str(uniqueid.lower())
        super(Post, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )

    def gallery_images(self) -> models.Model:
        return Gallery.objects.filter(post=self)

    def title_len_count(self) -> int:
        return len(self.title)

    def galley_img_count(self) -> int:
        return Gallery.objects.filter(post=self).count()

    def post_comments(self) -> List[models.Model]:
        comments = Comment.objects.filter(post=self, active=True)
        return comments

    def post_comments_count(self) -> int:
        comments_count = Comment.objects.filter(post=self, active=True).count()
        return comments_count


class Gallery(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='gallery', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.post)

    class Meta:
        verbose_name_plural = 'Gallery'

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 30px;" />'
            % (self.image)
        )


class FriendRequest(BaseModel):
    fid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='request_sender',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='request_receiver',
    )
    status = models.CharField(max_length=10, default='pending', choices=FRIEND_REQUEST)

    def __str__(self) -> str:
        return f'{self.sender}'

    class Meta:
        verbose_name_plural = 'Friend Request'


class Friend(BaseModel):
    fid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    def __str__(self) -> str:
        return f'{self.user.username}'

    class Meta:
        verbose_name_plural = 'Friend'


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True, null=True)
    cid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name_plural = 'Comment'

    def comment_replies(self) -> List[models.Model]:
        comment_replies = ReplyComment.objects.filter(comment=self, active=True)
        return comment_replies


class ReplyComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=True, null=True)
    cid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name_plural = 'Reply Comment'


class Notification(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='noti_user'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='noti_sender',
    )
    post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='noti_post'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='noti_comment',
    )
    notification_type = models.CharField(
        max_length=100, choices=NOTIFICATION_TYPE, default='none'
    )
    is_read = models.BooleanField(default=False)
    nid = ShortUUIDField(length=10, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz')

    class Meta:
        verbose_name_plural = 'Notification'

    def __str__(self) -> str:
        return f'{self.user.username} - {self.notification_type}'


class Group(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    memebers = models.ManyToManyField(User, blank=True, related_name='memebers')

    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default='everyone', choices=VISIBILITY)
    gid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Group'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())
        super(Group, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )

    def memeber_count(self) -> int:
        return self.memebers.all().count()


class GroupPost(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default='everyone', choices=VISIBILITY)
    pid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    likes = models.ManyToManyField(User, blank=True, related_name='group_post_likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> int:
        return self.title

    class Meta:
        verbose_name_plural = 'Group Post'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title) + '-' + str(uniqueid.lower())
        super(GroupPost, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )


class Page(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name='page_followers')
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default='everyone', choices=VISIBILITY)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    gid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Page'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())
        super(Page, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )

    def followers_count(self) -> int:
        return self.followers.all().count()


class PagePost(BaseModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default='everyone', choices=VISIBILITY)
    pid = ShortUUIDField(
        length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz123'
    )
    likes = models.ManyToManyField(User, blank=True, related_name='page_post_likes')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Group Post'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title) + '-' + str(uniqueid.lower())
        super(PagePost, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )


class ChatMessage(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='chat_user'
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sender'
    )
    reciever = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reciever'
    )
    message = models.CharField(max_length=100000)
    is_read = models.BooleanField(default=False)
    mid = ShortUUIDField(length=10, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz')

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name_plural = 'Personal Chat'

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )


class GroupChat(BaseModel):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    images = models.FileField(upload_to='group_chat', blank=True, null=True)
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='group_host'
    )
    members = models.ManyToManyField(User, related_name='group_chat_members')
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'Group Chat'

    def save(self, *args: Any, **kwargs: Any) -> None:
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.name) + '-' + str(uniqueid.lower())
        super(GroupChat, self).save(*args, **kwargs)

    def thumbnail(self) -> mark_safe:
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />'
            % (self.image)
        )

    def last_message(self) -> List[models.Model]:
        last_message = (
            GroupChatMessage.objects.filter(groupchat=self).order_by('-id').first()
        )
        return last_message


class GroupChatMessage(BaseModel):
    groupchat = models.ForeignKey(
        GroupChat, on_delete=models.SET_NULL, null=True, related_name='group_chat'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='group_chat_message_sender',
    )
    message = models.CharField(max_length=100000)
    is_read = models.BooleanField(default=False)
    mid = ShortUUIDField(length=10, max_length=25, alphabet='abcdefghijklmnopqrstuvxyz')

    def __str__(self) -> str:
        return self.groupchat.name

    class Meta:
        verbose_name_plural = 'Group Chat Messages'
