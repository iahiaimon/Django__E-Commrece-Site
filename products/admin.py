from django.contrib import admin

from .models import category , product , product_image , review , Cart , CartItem
# Register your models here.

admin.site.register([category , product_image , review , Cart , CartItem])

class ProductImageInline(admin.TabularInline):  # or use StackedInline
    model = product_image
    extra = 1  # how many blank image forms to show

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(product, ProductAdmin)
