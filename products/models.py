from django.db import models
from django.utils.text import slugify

# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank= True , null= True)
    image = models.ImageField(upload_to="Categories" , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self , *args , **keyargs):
        self.slug = slugify(self.name)
        super().save(*args , **keyargs)