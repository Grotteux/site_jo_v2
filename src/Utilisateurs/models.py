import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modèle pour gérer les clés utilisateur
class KeyUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_key(sender, instance, created, **kwargs):
    if created:
        KeyUser.objects.create(user=instance, user_key=str(uuid.uuid4()))

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_key(sender, instance, **kwargs):
    instance.keyuser.save()

