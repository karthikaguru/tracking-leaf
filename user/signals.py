from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
 
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,username=instance.username)
 

@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def save_profile(sender, instance, **kwargs):
        profile = instance.profile
        profile.username = instance.username
        profile.save()





        