from django.conf import settings
from django.db import models

# offers/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # your custom fields here
    pass


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(max_length=100, unique = True)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Tag(models.Model):
        name = models.CharField(max_length=100, unique = True)
        class Meta:
            verbose_name = 'Tag'
            verbose_name_plural = 'Tag'
            ordering = ['name']

        def __str__(self):
            return self.name


class Offer(models.Model):
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    category = models.ForeignKey(
    Category,
    on_delete=models.PROTECT,
    related_name = 'offers',)


    tags = models.ManyToManyField(

    Tag,
    related_name = 'offers',
            
    )

    author = models.ForeignKey(

        settings.AUTH_USER_MODEL ,
        on_delete = models.CASCADE,
        related_name='offers',
            
          
     )


    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
