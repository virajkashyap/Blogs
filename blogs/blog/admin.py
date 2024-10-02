from django.contrib import admin

# Register your models here.
from blog.models import blog_user 
from blog.models import Blog 
from blog.models import Tag 
from blog.models import Comment

admin.site.register(blog_user) 
admin.site.register(Blog ) 
admin.site.register(Tag) 
admin.site.register(Comment) 