# apps/users/models.py  (or wherever your custom User lives)
from django.db import models
from django.utils import timezone


class Account(models.Model):
    name = models.CharField(max_length=150, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return self.name or f"Account {self.pk}"
