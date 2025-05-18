from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import product, Cart, CartItem
from .forms import productForm
from .utils import get_session_key


from .models import category, product, product_image, review

# Create your views here.


def home(request):
    products = product.objects.all()
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    categories = category.objects.annotate(product_count=Count("products"))

    for p in products:
        if p.discount_parcentage:
            p.final_price = p.price - (p.price * p.discount_parcentage / 100)
        else:
            p.final_price = p.price

        p.is_new = (timezone.now() - p.created_at) <= timedelta(days=1)

    context = {
        "categories": categories,
        "MEDIA_URL": settings.MEDIA_URL,
        "product": products,
        "cart": cart,
        "total": total,
    }

    return render(request, "home.html", context=context)


def category_products(request, category_slug):
    category = get_object_or_404(category, slug=category_slug)

    products = product.objects.filter(category=category)

    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
        "category": category,
    }
    return render(request, "category.html", context)


def product_details(request, slug):
    products = get_object_or_404(product, slug=slug)
    context = {
        "products": products,
    }

    return render(request, "product_details.html", context=context)


def add_to_cart(request, product_id):
    item = get_object_or_404(product, id=product_id)
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)] = {
            "name": item.name,
            "price": float(item.price),
            "image": (
                item.product_image.first().image.url
                if item.product_image.exists()
                else ""
            ),
            "quantity": 1,
        }
    print(cart)
    request.session["cart"] = cart
    return redirect("home")


def cart_view(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render(request, "cart.html", {"cart": cart, "total": total})


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
    return redirect("home")


