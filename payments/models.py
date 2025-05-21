from django.db import models

from accounts.models import CustomUser


# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, related_name="payments" , null=True , on_delete=models.SET_NULL)
    payment_id = models.CharField(max_length=255 , null=True , blank=True)
    payment_method = models.CharField(max_length=255 , null=True , blank=True)
    amount_paid = models.DecimalField(max_digits=10 , decimal_places=2)
    status = models.CharField(max_length=255 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name="orders" , null=True , on_delete=models.SET_NULL)
    payment = models.ForeignKey(Payment, related_name="orders" , null=True , on_delete=models.CASCADE)

    order_number = models.CharField(max_length=255 , null=True , blank=True)
    order_note = models.CharField(max_length=255 , null=True , blank=True)
    order_total = models.DecimalField(max_digits=10 , decimal_places=2)
    address = models.CharField(max_length=255 , null=True , blank=True)

    is_orderd = models.BooleanField(default=False , null=False , blank=False)
    status = models.CharField(max_length=255 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="order_products" , on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name="order_products" , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=10 , decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
