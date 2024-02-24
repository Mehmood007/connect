from django.http import HttpRequest
from django.shortcuts import redirect


class AuthenticatedUserMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> redirect or None:
        if request.user.is_anonymous:
            return redirect('sign-up')
        return super().dispatch(request, *args, **kwargs)
