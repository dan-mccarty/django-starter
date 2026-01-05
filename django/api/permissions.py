# apps/api_keys/permissions.py
from rest_framework.permissions import BasePermission


class HasApiScope(BasePermission):
    required_scopes: list[str] = []

    def has_permission(self, request, view):
        api_key = getattr(request, "api_key", None)
        if not api_key:
            return False
        required = getattr(view, "required_scopes", self.required_scopes) or []
        return all(api_key.has_scope(s) for s in required)
