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
from .forms import CustomUserForm , ProfileForm
from .utils import send_verification_email
from products.views import home

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
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    # reviews = Review.objects.filter(user=request.user).select_related("product")
    return render(request, "user_profile.html", {"orders": orders})


@login_required
def edit_profile(request):
    user_form = CustomUserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user)

    if request.method == "POST":
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("user_profile")

    return render(
        request,
        "edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
