from django.db import models
from django.utils import timezone

# Models for Profile:
class Profile(models.Model):
    user_token = models.CharField(max_length=150)
    login_token = models.CharField(max_length=150)
    name = models.CharField(max_length=100)
    d_o_b = models.DateField(default=timezone.now)
    nick_name = models.CharField(max_length=150)
    image_url = models.URLField(max_length=200)
    soft_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
