import shortuuid
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.views import View

from utils.authenticated_user import AuthenticatedUserMixin

from .models import Comment, Post, ReplyComment


# '/post_detail'
class PostDetailView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest, slug: str) -> render:
        post = Post.objects.get(active=True, visibility="Everyone", slug=slug)
        context = {"p": post}
        return render(request, "core/post-detail.html", context)


# '/create_post'
class CreatePostView(AuthenticatedUserMixin, View):
    def post(self, request: HttpRequest) -> JsonResponse:
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')
        uuid_key = shortuuid.uuid()
        unique_id = uuid_key[:4]
        post = Post(
            title=title,
            visibility=visibility,
            image=image,
            user=request.user,
            slug=slugify(title) + '-' + unique_id.lower(),
        )
        post.save()

        return JsonResponse(
            {
                'post': {
                    'title': post.title,
                    'image_url': post.image.url,
                    "full_name": post.user.profile.full_name,
                    "profile_image": post.user.profile.image.url,
                    "date": timesince(post.created_at),
                    "id": post.id,
                }
            }
        )


# '/like_post'
class LikePostView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        id = request.GET.get('id')
        post = Post.objects.get(id=id)
        user = request.user
        is_liked = False

        if user in post.likes.all():
            post.likes.remove(user)
            is_liked = False
        else:
            post.likes.add(user)
            is_liked = True

        data = {'bool': is_liked, 'likes': post.likes.all().count()}
        return JsonResponse({'data': data})


# '/comment_on_post'
class CommentOnPostView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        id = request.GET.get('id')
        comment = request.GET.get('comment')
        post = Post.objects.get(id=id)
        user = request.user
        comment_count = Comment.objects.filter(post=post).count()

        new_comment = Comment(post=post, user=user, comment=comment)
        new_comment.save()

        data = {
            'bool': True,
            'comment': comment,
            'profile_image': user.profile.image.url,
            'date': timesince(new_comment.created_at),
            'comment_id': new_comment.id,
            'post_id': post.id,
            'comment_count': (comment_count + 1),
        }

        return JsonResponse({'data': data})


# '/like_comment'
class LikeCommentView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        id = request.GET.get('id')
        comment = Comment.objects.get(id=id)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            is_liked = False
        else:
            comment.likes.add(user)
            is_liked = True

        data = {'bool': is_liked, 'likes': comment.likes.all().count()}

        return JsonResponse({'data': data})


# '/reply_comment'
class ReplyCommentView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        id = request.GET['id']
        reply = request.GET['reply']

        comment = Comment.objects.get(id=id)
        user = request.user

        new_reply = ReplyComment.objects.create(comment=comment, reply=reply, user=user)

        data = {
            "bool": True,
            'reply': new_reply.reply,
            "profile_image": new_reply.user.profile.image.url,
            "date": timesince(new_reply.created_at),
            "reply_id": new_reply.id,
            "post_id": new_reply.comment.post.id,
        }
        return JsonResponse({"data": data})


# '/delete_comment'
class DeleteCommentView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> JsonResponse:
        id = request.GET['id']

        comment = Comment.objects.get(id=id, user=request.user)
        comment.delete()

        data = {
            "bool": True,
        }
        return JsonResponse({"data": data})
