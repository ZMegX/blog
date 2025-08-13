# blog/models.py
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):

        return self.title
    def get_absolute_url(self): # Change here
        return reverse('blog:post_detail', kwargs={'pk': self.pk}) 

class Comment(models.Model):
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.author} on '{self.post}'"
    
