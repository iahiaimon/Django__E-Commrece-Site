from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from products.models import Cart, CartItem, product
from products.utils import get_session_key
from .models import Order, OrderProduct, Payment
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_python_api import SSLCSession
from django.urls import reverse

# from sslcommerz_lib import SSLCSession
from products.models import product

import datetime
import random


def place_order(request):
    # Get cart
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session_id=get_session_key(request))
    except Cart.DoesNotExist:
        return redirect("home")

    # Get cart products
    cart_products = CartItem.objects.filter(cart=cart).select_related("product")

    if not cart_products.exists():
        return redirect("home")

    quantity = 0
    total = 0
    cart_items = []

    for item in cart_products:
        item_total = item.quantity * item.product.price
        cart_items.append(
            {
                "product": item.product,
                "quantity": item.quantity,
                "item_total": item_total,
            }
        )
        quantity += item.quantity
        total += item_total

    delivery = getattr(settings, "DELIVERY_CHARGE", 0)
    grand_total = total + delivery

    # Handle form POST (placing order)
    if request.method == "POST":
        payment_option = request.POST.get("payment_method", "cash")

        try:
            current_user = request.user
            current_date = datetime.date.today()
            order_number = current_date.strftime("%Y%m%d%H%M%S") + str(
                random.randint(1000, 9999)
            )

            order = Order.objects.create(
                user=current_user,
                address=current_user.address,
                order_note=request.POST.get("order_note", ""),
                order_total=grand_total,
                status="Pending",
                order_number=order_number,
            )

            for item in cart_products:
                OrderProduct.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                )

                # Update stock
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()

            # Clear the cart
            cart_products.delete()

            # Redirect based on payment method
            if payment_option == "cash":
                return redirect("order_complete")
            elif payment_option == "sslcommerz":
                return redirect("payment")

        except Exception as e:
            return HttpResponse("An error occurred: " + str(e))

    # Show checkout page
    context = {
        "cart_items": cart_items,
        "quantity": quantity,
        "total": total,
        "grand_total": grand_total,
        "delivery_charge": delivery,
    }

    return render(request, "checkout.html", context)


def payment(request):
    user = request.user
    order = Order.objects.filter(user=user, status="Pending").last()

    if not order:
        return redirect("home")

    mypayment = SSLCSession(
        sslc_is_sandbox=settings.SSLCOMMERZ_IS_SANDBOX,
        sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
        sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS,
    )

    # ✅ Use a named URL pattern for status (make sure it's defined in urls.py)
    status_url = request.build_absolute_uri(reverse("payment_status"))

    mypayment.set_urls(
        success_url=status_url,
        fail_url=status_url,
        cancel_url=status_url,
        ipn_url=status_url,
    )

    num_of_items = OrderProduct.objects.filter(order=order).count()

    mypayment.set_product_integration(
        total_amount=order.order_total,
        currency="BDT",
        product_category="clothing",
        product_name="Order#" + order.order_number,
        num_of_item=num_of_items,
        shipping_method="YES",
        product_profile="general",
    )

    # ✅ Corrected user fields
    mypayment.set_customer_info(
        name=user.get_full_name(),
        email=user.email,
        address1=user.address or "N/A",
        address2="",
        city="Dhaka",
        postcode="1000",
        country="Bnagladesh",
        phone=user.phone,
    )

    # ✅ Shipping info (use order address or user address)
    mypayment.set_shipping_info(
        shipping_to=user.get_full_name(),
        address=user.address or "N/A",
        city="Dhaka",
        postcode="1000",
        country="Bnagladesh",
    )

    response_data = mypayment.init_payment()

    if response_data["status"] == "FAILED":
        order.status = "Failed"
        order.save()

    # return redirect(response_data["GatewayPageURL"])

    response_data = mypayment.init_payment()

    # Debug: Print or log the response
    print("SSLCOMMERZ Response:", response_data)

    if response_data.get("status") == "FAILED":
        order.status = "Failed"
        order.save()
        return HttpResponse(
            "Payment initiation failed: "
            + response_data.get("failedreason", "Unknown reason")
        )

    # Check if GatewayPageURL exists before redirecting
    if "GatewayPageURL" not in response_data:
        return HttpResponse(
            "SSLCOMMERZ failed to return a payment URL. Full response: "
            + str(response_data)
        )

    # Otherwise redirect to the payment gateway
    return redirect(
        response_data[" https://sandbox.sslcommerz.com/gwprocess/v3/api.php"]
    )


@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        payment_data = request.POST
        if payment_data["status"] == "VALID":
            val_id = payment_data["val_id"]
            tran_id = payment_data["tran_id"]

            order = Order.objects.filter(user=request.user).last()

            payment = Payment.objects.create(
                user=request.user,
                payment_id=val_id,
                payment_method="SSLCommerz",
                amount_paid=order.order_total,
                status="Completed",
            )

            order.status = "Completed"
            order.payment = payment
            order.save()

            # CartItems will be automatically deleted
            Cart.objects.filter(user=request.user).delete()

            context = {
                "order": order,
                "transaction_id": tran_id,
            }
            return render(request, "order_success.html", context)

        else:
            return render(request, "payment_failed.html")


def order_complete(request):
    return render(request, "order_success.html")
