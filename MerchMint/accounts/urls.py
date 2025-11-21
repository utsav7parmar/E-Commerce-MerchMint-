"""
URL configuration for MerchMint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # Register
    path('register/', views.register, name='register'),

    # Login
    path('login/', views.login_view, name='login'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Edit Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Forgot Password
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # Reset Password (OTP verify page)
    path('reset-password/', views.reset_password, name='reset_password'),

    # Logout 
    path('logout/', views.logout_view, name='logout'), 
]
