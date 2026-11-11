from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):

  user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # The image field connects directly to Cloudinary storage
  profile_image = CloudinaryField('image', folder='profile_pics/', blank=True, null=True)

  def __cl_init__(self):
        return f"{self.user.username}'s Profile"