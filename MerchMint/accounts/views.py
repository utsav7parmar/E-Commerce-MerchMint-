from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import random

from .models import User

# REGISTER USER

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password match validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        # Ensure unique email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Create user
        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=make_password(password),
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")

# LOGIN USER

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

        if check_password(password, user.password):
            request.session["user_id"] = user.id
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

    return render(request, "accounts/login.html")

# PROFILE PAGE

def profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    return render(request, "accounts/profile.html", {"user": user})

# EDIT PROFILE

def edit_profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.mobile = request.POST.get("mobile")
        user.bio = request.POST.get("bio")
        user.address = request.POST.get("address")

        if "profile_image" in request.FILES:
            user.profile_image = request.FILES["profile_image"]

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "accounts/edit_profile.html", {"user": user})

# FORGOT PASSWORD

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect("forgot_password")

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        # You can integrate email sending later
        messages.success(request, f"Your OTP is: {otp}")  # temporary
        return redirect("reset_password")

    return render(request, "accounts/forgot_password.html")

# RESET PASSWORD PAGE

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid Email.")
            return redirect("reset_password")

        if user.otp != otp:
            messages.error(request, "Invalid OTP.")
            return redirect("reset_password")

        user.password = make_password(new_password)
        user.otp = None
        user.save()

        messages.success(request, "Password reset successful.")
        return redirect("login")

    return render(request, "accounts/reset_password.html")

# LOGOUT USER

def logout_view(request):
    request.session.flush()
    return redirect("login")
