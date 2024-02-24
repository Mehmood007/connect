from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from utils.authenticated_user import AuthenticatedUserMixin

from .models import Post


# '/'
class FeedView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'core/index.html', context)
