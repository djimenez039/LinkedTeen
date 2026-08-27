from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('organization', 'Organization'),
    ] 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Create your models here.
