from django.shortcuts import render
from django.db.models import Count
from django.conf import settings

from .models import product
from .forms import productForm


from .models import category , product , product_image , review
# Create your views here.


def home(request):
    products = product.objects.all()
    categories = category.objects.annotate(product_count = Count(product))

    contex = {
        'categories': categories,
        "MEDIA_URL": settings.MEDIA_URL,
        "product":products
    }
    return render(request, 'home.html' , context=contex )