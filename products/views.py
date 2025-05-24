from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import product, Cart, CartItem
from .forms import productForm, ReviewForm
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


def category_products(request, slug):
    categoris = get_object_or_404(category, slug=slug)

    products = product.objects.filter(categoris=categoris)

    # paginator = Paginator(products, 6)
    # page = request.GET.get("page")
    # paged_products = paginator.get_page(page)

    context = {
        # "products": paged_products,
        "products": products,
        "category": categoris,
    }
    return render(request, "category.html", context)


def product_details(request, slug):
    product_obj = get_object_or_404(product, slug=slug)
    reviews = review.objects.filter(product=product_obj).order_by("-created_at")

    form = ReviewForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviews = form.save(commit=False)
            reviews.user = request.user
            reviews.product = product_obj
            reviews.save()
            return redirect("product_details", slug=slug)

    context = {
        "products": product_obj,
        "reviews": reviews,
        "form": form,
    }

    return render(request, "product_details.html", context)


@login_required
def add_to_cart(request, product_id):
    item = get_object_or_404(product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()

    return redirect("home")


def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = get_session_key(request)
        cart, _ = Cart.objects.get_or_create(session_id=session_key)

    cart_items_qs = CartItem.objects.filter(cart=cart).select_related("product")
    cart_items = []
    total = 0

    for item in cart_items_qs:
        item_total = item.quantity * item.product.price
        cart_items.append(
            {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "image": (
                    item.product.product_image.first().image.url
                    if item.product.product_image.exists()
                    else ""
                ),
                "total": item_total,
            }
        )
        total += item_total

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "cart.html", context)


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        print("problem found")
    else:
        session_key = get_session_key(request)
        cart = Cart.objects.filter(session_id=session_key).first()

    if cart:
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return redirect("cart_view")


def update_cart(request, product_id, action):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_id=get_session_key(request)).first()

    if not cart:
        return redirect("cart_view")

    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()

    return redirect("cart_view")


# def user_review(request , product_id):
#     product_obj = get_object_or_404(product, id=product_id)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.product = product_obj
#             review.save()
#             return redirect('user_profile')  # Or product detail page
#     else:
#         form = ReviewForm()

#     return render(request, 'reviews/write_review.html', {'form': form, 'product': product_obj})
