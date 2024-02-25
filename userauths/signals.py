from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(
    sender: User, instance: User, created: bool, **kwargs
) -> None:
    if created:
        Profile.objects.create(user=instance)
    else:
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
