from typing import Any
from django.db import models
from django.contrib.auth.models import User
from main.models import PostImage

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField()
    # comments



class BlogPostImage(PostImage):
    blog_post = models.ForeignKey(BlogPost, related_name='blog_post_image', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='blog_post_images', blank=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.blog_post} {self.images}'

