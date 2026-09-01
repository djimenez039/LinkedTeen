from django.conf import settings
from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    needs = models.TextField(blank=True)
    skills_needed = models.TextField(blank=True)
    time_commitment = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
