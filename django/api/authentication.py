# api/authentication.py
import hashlib

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import ApiKey  # adjust if your app label differs


class AccountApiKeyAuthentication(BaseAuthentication):
    """
    Authenticate via:
      Authorization: Bearer <raw_api_key>

    Sets:
      request.account -> Account
      request.api_key -> ApiKey
    """

    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if not header:
            return None  # allow other auth methods or public endpoints

        try:
            scheme, raw = header.split(" ", 1)
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format.")

        if scheme != self.keyword:
            return None

        raw = raw.strip()
        if not raw:
            raise AuthenticationFailed("Empty API key.")

        prefix = raw[:12]
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        api_key = (
            ApiKey.objects.select_related("account")
            # .prefetch_related("scopes")
            .filter(key_prefix=prefix, key_hash=digest, is_active=True)
            .first()
        )
        if not api_key:
            raise AuthenticationFailed("Invalid API key.")

        if not api_key.is_domain_allowed(request.get_host()):
            raise AuthenticationFailed("Domain not allowed.")

        # attach principal
        request.account = api_key.account
        request.api_key = api_key

        # optional: last-used tracking
        ApiKey.objects.filter(pk=api_key.pk).update(last_used_at=timezone.now())

        # API calls do NOT authenticate as a Django user
        return (AnonymousUser(), api_key)
