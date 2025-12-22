from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from .services import send_verification_email


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("email", "is_email_verified", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_email_verified")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Email Verification"), {"fields": ("is_email_verified",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_email_verified",
                ),
            },
        ),
    )

    # --------------------------
    # Override save_model to send email verification
    # --------------------------
    def save_model(self, request, obj, form, change):
        # If the user is new (not change) and email not verified
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        if is_new and not obj.is_email_verified:
            send_verification_email(obj, request)
