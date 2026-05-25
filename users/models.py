from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    profile_picture = ResizedImageField(
        size=[300, 300],
        quality=75,
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    def __str__(self):
        return self.full_name
