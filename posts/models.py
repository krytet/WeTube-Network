from typing import Text

from django.contrib.auth import get_user_model
from django.db import models

from group.models import Group

User = get_user_model()



class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="posts")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'comments')
    text = models.TextField()
    created = models.TimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    
# Create your models here.

