from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from payments.models import Order


from .models import CustomUser
from .forms import CustomUserForm, ProfileForm
from .utils import send_verification_email
from products.views import home
from products.models import review

# Create your views here.


def user_singup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            send_verification_email(request, user)
            messages.info(
                request, "A verification email has been sent to your email address"
            )

            return redirect("login")
        else:
            print(form.errors)

    else:
        form = CustomUserForm()

    return render(request, "singup.html", {"form": form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        messages.success(request, "Email verified! You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "Verification link is invalid or has expired.")
        return render(request, "singup.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Invalid username or password")
        elif not user.is_verified:
            messages.error(request, "Your email is not verified")
        else:
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect("home")

    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("login")


@login_required
def user_profile(request):
    # orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            "order_products__product"
        )  # Load related products efficiently
        .order_by("-created_at")[:5]
    )
    # reviews = review.objects.filter(user=request.user).select_related("product")
    reviews = (
        review.objects.filter(user = request.user)
        .select_related(
            "product"
        )
        .order_by("created_at")
        )
    context = {
        "orders": orders,
        "reviews": reviews,
    }
    return render(request, "user_profile.html", context)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            for field in form.cleaned_data:
                new_value = form.cleaned_data.get(field)
                if new_value not in [None, ""]:
                    setattr(user, field, new_value)

            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("user_profile")
    else:
        form = CustomUserForm(instance=user)

    return render(request, "edit_profile.html", {"form": form})
