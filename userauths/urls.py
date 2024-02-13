from django.urls import path

from .views import SignInView, SignUpView, SingOutView

urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', SingOutView.as_view(), name='sign-out'),
]
