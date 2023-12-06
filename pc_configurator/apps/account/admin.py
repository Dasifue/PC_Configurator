from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "full_name")
    search_fields = ("username", "email")
    empty_value_display = "???"
    fieldsets = (
        ("Base", {
            "fields": ("username", "email", "first_name", "last_name", "image", "date_joined")
            }
        ),
        ("Advanced", {
            "fields": ("is_staff", "is_superuser", "password")
        })
    )