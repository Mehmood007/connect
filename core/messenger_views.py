from django.db.models import Count, F, FloatField, OuterRef, Q, Subquery, Sum
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from userauths.models import User
from utils.authenticated_user import AuthenticatedUserMixin

from .models import ChatMessage


# 'core/inbox'
class InboxView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest) -> render:
        user_id = request.user

        chat_message = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) | Q(reciever__sender=user_id)
                )
                .distinct()
                .annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id)
                            | Q(reciever=OuterRef('id'), sender=user_id)
                        )
                        .order_by('-id')[:1]
                        .values_list('id', flat=True)
                    )
                )
                .values_list('last_msg', flat=True)
                .order_by("-id")
            )
        ).order_by("-id")

        context = {
            'chat_message': chat_message,
        }
        return render(request, 'chat/inbox.html', context)


# 'core/inbox'
class InboxDetailView(AuthenticatedUserMixin, View):
    def get(self, request: HttpRequest, username: str) -> render:
        user_id = request.user
        message_list = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) | Q(reciever__sender=user_id)
                )
                .distinct()
                .annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id)
                            | Q(reciever=OuterRef('id'), sender=user_id)
                        )
                        .order_by('-id')[:1]
                        .values_list('id', flat=True)
                    )
                )
                .values_list('last_msg', flat=True)
                .order_by("-id")
            )
        ).order_by("-id")

        sender = request.user
        receiver = User.objects.get(username=username)
        receiver_details = User.objects.get(username=username)

        messages_detail = ChatMessage.objects.filter(
            Q(sender=sender, reciever=receiver) | Q(sender=receiver, reciever=sender)
        ).order_by("created_at")

        messages_detail.update(is_read=True)

        if messages_detail:
            r = messages_detail.first()
            reciever = User.objects.get(username=r.reciever)
        else:
            reciever = User.objects.get(username=username)

        context = {
            'message_detail': messages_detail,
            "reciever": reciever,
            "sender": sender,
            "receiver_details": receiver_details,
            "message_list": message_list,
        }
        return render(request, 'chat/inbox_detail.html', context)
