import shortuuid
from django.http import HttpRequest, JsonResponse
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.views import View

from utils.authenticated_user import AuthenticatedUserMixin

from .models import Post


# 'create_post'
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
