from django.http import HttpRequest
from django.shortcuts import redirect


class AnonymousUserMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> redirect or None:
        if request.user.is_authenticated:
            return redirect('feed')
        return super().dispatch(request, *args, **kwargs)
