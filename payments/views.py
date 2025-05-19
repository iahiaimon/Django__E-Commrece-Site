from django.shortcuts import render, get_object_or_404 , redirect
from django.conf import settings
from .models import Order, Payment, OrderProduct
from products.models import Cart ,CartItem
from products.utils import get_session_key

# Create your views here.


def order_product(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
    else:
        cart = get_object_or_404(Cart, session_key=get_session_key())

    cart_products =  CartItem.objects.filter(cart=cart).select_related("products")
    if CartItem.count()==0:
        return redirect("home")
    
    total = 0
    for cart_product in cart_products:
        total += cart_product.products.price * cart_product.quantity
        quantity += cart_product.quantity

    contex = {
        "total" : total ,
        "quantity" : quantity ,
        "cart_items": cart_products ,
        "grand_total" : total + settings.DELIVERY_CHARGR
    }

    return render(request , "checkout.html" , {"cart":cart} )
