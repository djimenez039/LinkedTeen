from django.conf import settings
from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    needs = models.TextField(blank=True)
    skills_needed = models.TextField(blank=True)
    time_commitment = models.CharField(max_length=120, blank=True)
    availability = models.CharField(max_length=120, blank=True)
    presidents = models.CharField(max_length=255, blank=True, help_text='Separate multiple presidents with commas.')
    sponsor = models.CharField(max_length=150, blank=True)
    keywords = models.TextField(blank=True, help_text='Comma-separated keywords describing this club.')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_posts')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
