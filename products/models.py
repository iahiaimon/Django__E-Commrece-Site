from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser

# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank= True , null= True , max_length=255)
    image = models.ImageField(upload_to="Categories" , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self , *args , **keyargs):
        self.slug = slugify(self.name)
        super().save(*args , **keyargs)


class product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , blank= True , null= True , max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    discount_parcentage = models.DecimalField(max_digits=10 , decimal_places=2)

    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    unit = models.CharField(max_length=100 , null=True , blank=True)
    rating = models.DecimalField(max_digits=10 , decimal_places=2 , null=True , blank=True)

    category = models.ForeignKey(category , related_name="products" , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self , *args , **keyargs):
        self.slug = slugify(self.name)
        super().save(*args , **keyargs)


class product_image(models.Model):
    product = models.ForeignKey(product , related_name="product_image" , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Product_Image")


    def __str__(self):
        return f"Image for {self.product.name}"
    

class review(models.Model):
    product = models.ForeignKey(product , related_name="reviews" , on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser , related_name="reviews" , on_delete=models.CASCADE)

    rating = models.DecimalField(max_digits=10 , decimal_places=2)
    reviews = models.TextField()

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.product.name}"