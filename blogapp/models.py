from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings   

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_img/', blank=True, null=True)
    facebook =  models.URLField(max_length= 255, blank=True, null=True)
    youtube =  models.URLField(max_length= 255, blank=True, null=True)
    instagram =  models.URLField(max_length= 255, blank=True, null=True)
    twitter =  models.URLField(max_length= 255, blank=True, null=True)
    linkedin =  models.URLField(max_length= 255, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )

    def __str__(self):
        return self.username
    

class Blog(models.Model):
    CATEGORY = (
        ('Technology', 'Technology'),
        ("Economy", "Economy"),
        ("Business", "Business"),
        ("Sports", "Sports"),
        ('Lifestyle', 'Lifestyle'),
    )

    title=models.CharField(max_length=255)
    slug= models.SlugField(max_length=255,unique=True,blank=True)
    content= models.TextField()
    author= models.ForeignKey()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    published_time= models.DateTimeField(blank=True,null=True)
    is_draft= models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=CATEGORY, blank=True, null=True)
    featured_image = models.ImageField(upload_to='blog_img', blank=True, null=True)

class Meta:
    ordering = ['-created_at']