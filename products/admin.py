from django.contrib import admin

from .models import category , product , product_image , review
# Register your models here.

admin.site.register([category , product , product_image , review])