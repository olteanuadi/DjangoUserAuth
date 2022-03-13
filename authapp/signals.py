from django.contrib.auth.forms import UserChangeForm
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserRegistrationModel


@receiver(post_save, sender=User)
def creater_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserRegistrationModel.objects.create(user=instance)
        profile.save()

# @receiver(post_save, sender=User)
# def create_post(sender, instance, created, **kwargs):
#     if created:
#         post = UserPost.objects.create(post_text=instance)
#         post.save()

