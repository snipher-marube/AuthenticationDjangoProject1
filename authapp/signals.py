from django.db.models.signals import pre_save
from django.contrib.auth.models import User

def update_username(sender, instance, **kwargs):
    instance.username = instance.email

pre_save.connect(update_username, sender=User)
