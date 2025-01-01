from django.db import models
from django.contrib.auth import get_user_model
from  django.contrib.auth.models import User



BlogUser = get_user_model()
# Create your models here.
class blog_user(models.Model):
    username=models.CharField(max_length=20,null=False )
    email=models.CharField(max_length=20,unique=True,null=False)
    password=models.CharField(max_length=20,null=False)

    def __str__(self):
        return self.username
    


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # Use TextField for larger content
    blog_image=models.ImageField(upload_to='blogs/', blank=True, null=True)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='blogs')# Assuming you have a Tag model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog,related_name='comment', on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='comment',  on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog.title}'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


