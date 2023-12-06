from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField("Image", upload_to="account/", default="account/default-avatar.jpg")
    email = models.EmailField("Email", unique=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
