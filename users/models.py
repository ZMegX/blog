from django.db import models
from django.contrib.auth.models import User
from PIL import Image # Change here from pillow import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, default='example@email.com')
    image = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username}'
