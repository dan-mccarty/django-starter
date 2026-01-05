# apps/api_keys/models.py
import hashlib, secrets
from django.db import models
from django.utils import timezone
from accounts.models import Account


class ApiKey(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="api_keys"
    )
    name = models.CharField(max_length=100)

    key_prefix = models.CharField(max_length=12, db_index=True, editable=False)
    key_hash = models.CharField(max_length=64, unique=True, editable=False)

    # Permissions for the key (scopes)
    scopes = models.JSONField(
        default=list, blank=True
    )  # e.g. ["orders:read", "orders:write"]

    allowed_domains = models.JSONField(blank=True, default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_used_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def generate_key() -> str:
        return f"api_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_key(raw_key: str) -> str:
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk:
            raw_key = self.generate_key()
            self.key_hash = self.hash_key(raw_key)
            self.key_prefix = raw_key[:12]
            self._raw_key_once = raw_key
        super().save(*args, **kwargs)

    def is_domain_allowed(self, host: str | None) -> bool:
        if not self.allowed_domains:
            return True
        if not host:
            return False
        return host.lower() in {d.lower() for d in self.allowed_domains}

    def has_scope(self, scope: str) -> bool:
        return scope in set(self.scopes or [])
