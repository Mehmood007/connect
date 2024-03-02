from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from userauths.models import User
from utils.authenticated_user import AuthenticatedUserMixin

from .models import FriendRequest, Post


# '/'
class FeedView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'core/index.html', context)


# '/add-friend/<id>'
class FriendRequestView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest, id: str) -> render:
        sender = request.user
        receiver_id = request.GET['id']
        bool = False

        if sender.id == int(receiver_id):
            return JsonResponse(
                {'error': 'You cannot send a friend request to yourself.'}
            )

        receiver = User.objects.get(id=receiver_id)

        try:
            friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
            if friend_request:
                friend_request.delete()
            bool = False
            return JsonResponse({'error': 'Cancelled', 'bool': bool})
        except FriendRequest.DoesNotExist:
            friend_request = FriendRequest(sender=sender, receiver=receiver)
            friend_request.save()
            bool = True

            return JsonResponse({'success': 'Sent', 'bool': bool})
