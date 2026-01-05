# accounts/auth_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailVerifiedBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Keep the default checks (is_active etc.)
        can = super().user_can_authenticate(user)
        if not can:
            return False

        # ✅ Always allow staff/superusers (admin login must work)
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return True

        # Normal users must be verified
        return getattr(user, "is_email_verified", False)
