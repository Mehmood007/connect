from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from core.models import FriendRequest, Post
from utils.anonymous_user import AnonymousUserMixin
from utils.authenticated_user import AuthenticatedUserMixin

from .forms import UserRegisterForm
from .models import Profile


# 'user/sign-up'
class SignUpView(AnonymousUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        form = UserRegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'userauths/sign-up.html', context)

    def post(self, request: HttpRequest) -> render or redirect:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=password)
            login(request, user)

            profile = Profile.objects.get(user=request.user)
            profile.full_name = full_name
            profile.phone = phone
            profile.gender = gender
            profile.save()

            messages.success(
                request,
                f'Hi {request.user.username}, your account have been created successfully.',
            )

            return redirect('feed')

        context = {
            'form': form,
        }

        messages.warning(request, 'Invalid credentials')
        return render(request, 'userauths/sign-up.html', context)


# 'user/sign-in'
class SignInView(AnonymousUserMixin, View):

    def post(self, request: HttpRequest) -> redirect:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(
                request,
                f'Hi {request.user.username}, your have logged in successfully.',
            )
            return redirect('feed')

        messages.warning(request, 'Invalid credentials')
        return redirect('sign-up')


# 'user/sign-out'
class SingOutView(View):
    def get(self, request: HttpRequest) -> redirect:
        if request.user.is_anonymous:
            messages.warning(request, 'You are not even logged in')
        else:
            logout(request)
            messages.success(request, 'You have successfully logged out')
        return redirect('sign-up')


# 'user/my-profile'
class MyProfileView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        profile = request.user.profile
        posts = Post.objects.filter(active=True, user=request.user)

        context = {
            "posts": posts,
            "profile": profile,
        }
        return render(request, "userauths/my-profile.html", context)


# 'user/profile/<username>'
class ProfileView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest, username: str) -> render:
        profile = Profile.objects.get(user__username=username)
        posts = Post.objects.filter(active=True, user=profile.user)

        # Send Friend Request Feature
        bool = False
        bool_friend = False

        sender = request.user
        receiver = profile.user
        bool_friend = False
        try:
            friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
            if friend_request:
                bool = True
            else:
                bool = False
        except:
            bool = False

        context = {
            "posts": posts,
            "bool_friend": bool_friend,
            "bool": bool,
            "profile": profile,
        }
        return render(request, "userauths/friend-profile.html", context)
