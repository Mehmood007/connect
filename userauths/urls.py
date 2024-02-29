from django.urls import path

from .views import MyProfileView, ProfileView, SignInView, SignUpView, SingOutView

urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', SingOutView.as_view(), name='sign-out'),
    path("my-profile", MyProfileView.as_view(), name="my-profile"),
    path("profile/<str:username>", ProfileView.as_view(), name="profile"),
]
