from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


# '/'
class FeedView(View):
    def get(self, request: HttpRequest) -> render:
        return render(request, 'core/index.html')
