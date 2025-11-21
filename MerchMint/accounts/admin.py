from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "mobile", "is_verified", "created_at")
    search_fields = ("email", "first_name", "last_name", "mobile")
    list_filter = ("is_verified", "created_at")
    ordering = ("-created_at",)

admin.site.register(User, UserAdmin)
