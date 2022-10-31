from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/img2.jpeg', upload_to='media/profile_pics', blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    phone = PhoneNumberField(blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

