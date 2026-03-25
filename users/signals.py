from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Line of code: Get the fields being updated
    update_fields = kwargs.get('update_fields')
    
    # Line of code: If ONLY last_login is changing, don't re-save the profile
    if update_fields and 'last_login' in update_fields and len(update_fields) == 1:
        return
        
    instance.profile.save()