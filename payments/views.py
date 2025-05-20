from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Cart, CartItem  # Update the import as needed
from products.utils import get_session_key  # Make sure you have this function


def place_order(request):
    # ✅ 1. Get Cart (by user or session)
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=get_session_key(request))
    except Cart.DoesNotExist as e:
        print(e)
        return redirect("home")  # No cart exists

    # ✅ 2. Get cart items
    cart_products = CartItem.objects.filter(cart=cart).select_related("product")

    # ✅ 3. Check if cart is empty
    if not cart_products.exists():
        print("Cart item is not found")
        return redirect("home")

    # ✅ 4. Calculate total and quantity
    quantity = 0
    total = 0
    for item in cart_products:
        quantity += item.quantity
        total += item.product.price * item.quantity

    # ✅ 5. Context
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_products,
        "grand_total": total + getattr(settings, "DELIVERY_CHARGE", 0),
    }

    return render(request, "checkout.html", context)
