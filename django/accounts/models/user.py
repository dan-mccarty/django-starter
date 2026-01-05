from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .account import Account
from ..managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    email = models.EmailField(unique=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="users",
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        db_index=True,
    )

    is_email_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_account_owner(self) -> bool:
        return self.role == self.Role.OWNER

    @property
    def is_account_admin(self) -> bool:
        return self.role in {self.Role.OWNER, self.Role.ADMIN}
