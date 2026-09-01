from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('organization', 'Organization'),
        ('mentor', 'Mentor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=120, blank=True)
    grade = models.CharField(max_length=30, blank=True)
    school = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    can_offer = models.TextField(blank=True)
    looking_for = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    causes = models.TextField(blank=True)
    availability = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username
