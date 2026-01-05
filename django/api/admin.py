# apps/api_keys/admin.py
from django.contrib import admin, messages
from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "account",
        "key_prefix",
        "is_active",
        "created_at",
        "last_used_at",
    )
    readonly_fields = ("key_prefix", "key_hash", "created_at", "last_used_at")

    def has_add_permission(self, request):
        return request.user.is_superuser  # or a custom permission

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        raw = getattr(obj, "_raw_key_once", None)
        if raw:
            messages.warning(request, f"Copy this API key now (shown once): {raw}")
