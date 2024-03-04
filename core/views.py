from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from userauths.models import User
from utils.authenticated_user import AuthenticatedUserMixin
from utils.notification import send_notification

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

            send_notification(receiver, sender, None, None, 'Friend Request')
            return JsonResponse({'success': 'Sent', 'bool': bool})


# '/accept-friend'
class AcceptFriendRequestView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        id = request.GET['id']

        receiver = request.user
        sender = User.objects.get(id=id)

        friend_request = FriendRequest.objects.filter(
            receiver=receiver, sender=sender
        ).first()

        receiver.profile.friends.add(sender)
        sender.profile.friends.add(receiver)

        friend_request.delete()

        data = {
            "message": "Accepted",
            "bool": True,
        }

        send_notification(receiver, sender, None, None, 'Friend Request Accepted')
        return JsonResponse({'data': data})


# '/reject-friend'
class RejectFriendRequestView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        id = request.GET['id']

        receiver = request.user
        sender = User.objects.get(id=id)

        friend_request = FriendRequest.objects.filter(
            receiver=receiver, sender=sender
        ).first()
        friend_request.delete()

        data = {
            "message": "Rejected",
            "bool": True,
        }
        return JsonResponse({'data': data})


# '/unfriend'
class UnfriendRequestView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        sender = request.user
        friend_id = request.GET['id']
        bool = False

        if sender.id == int(friend_id):
            return JsonResponse(
                {
                    'error': 'You cannot unfriend yourself, wait a minute how did you even send yourself a friend request?.'
                }
            )

        my_friend = User.objects.get(id=friend_id)

        if my_friend in sender.profile.friends.all():
            sender.profile.friends.remove(my_friend)
            my_friend.profile.friends.remove(sender)
            bool = True
            return JsonResponse({'success': 'Unfriend Successfull', 'bool': bool})


class BlockUserView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        id = request.GET['id']
        user = request.user
        friend = User.objects.get(id=id)

        if user.id == friend.id:
            return JsonResponse({'error': 'You cannot block yourself'})

        if friend in user.profile.friends.all():
            user.profile.blocked.add(friend)
            user.profile.friends.remove(friend)
            friend.profile.friends.remove(user)
        else:
            return JsonResponse(
                {'error': 'You cannot block someone that is not your friend'}
            )

        return JsonResponse({'success': 'User Blocked'})
