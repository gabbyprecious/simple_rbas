from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    OWNER = 0
    INVESTOR = 1
    ADMIN = 2
    WRITE = 3
    READ_ONLY = 4

    LEVEL_CHOICES = (
        (OWNER, "Owner"),
        (INVESTOR, "Investor"),
        (ADMIN, "Admin"),
        (WRITE, "Read/Write"),
        (READ_ONLY, "Read Only"),
    )

    level = models.SmallIntegerField(choices=LEVEL_CHOICES, db_index=True, default=READ_ONLY)