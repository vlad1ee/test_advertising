import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=150, unique=False, null=True,
                                blank=True)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        name = self.get_full_name()
        if not name:
            return self.email
        return name
