from django.db import models
from django.contrib.auth.models import AbstractUser


class CoreUser(AbstractUser):

    pass
    # Add Add Fields Later

    def __str__(self):
        return self.username
