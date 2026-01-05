from django.contrib.auth.base_user import BaseUserManager
from .models.account import Account


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, *, account=None, role=None, **extra_fields
    ):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        created_account = False
        if account is None:
            account = Account.objects.create(name="")
            created_account = True

        user = self.model(
            email=email,
            account=account,
            role=(
                self.model.Role.OWNER
                if created_account
                else (role or self.model.Role.USER)
            ),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        account = extra_fields.pop("account", None) or Account.objects.create(
            name="Admin"
        )
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email, password, account=account, role=self.model.Role.OWNER, **extra_fields
        )
