# blog/models.py
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# blog/models.py
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)  # unique=True optional but recommended
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "category"
            slug = base
            i = 1
            from .models import Category  # safe; same class
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)    
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
    
    def edit(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image
        self.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self): # Change here
        return reverse('blog:post_detail', kwargs={'pk': self.pk}) 

class Comment(models.Model):
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.author} on '{self.post}'"
    
