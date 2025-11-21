from django import forms
from .models import User
from django.contrib.auth.hashers import make_password, check_password

# REGISTER FORM

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        cleaned_data["password"] = make_password(password)
        return cleaned_data

# LOGIN FORM

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

# EDIT PROFILE FORM

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "mobile", "bio", "address", "profile_image"]

# FORGOT PASSWORD FORM

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

# RESET PASSWORD FORM

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput())
