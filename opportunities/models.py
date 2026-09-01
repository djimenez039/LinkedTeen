from django.db import models


class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ('internship', 'Internship'),
        ('volunteering', 'Volunteering'),
        ('competition', 'Competition'),
        ('research', 'Research'),
        ('summer_program', 'Summer Program'),
        ('scholarship', 'Scholarship'),
        ('hackathon', 'Hackathon'),
        ('leadership', 'Leadership'),
        ('event', 'Event'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='internship')
    description = models.TextField()
    skills_needed = models.TextField(blank=True)
    who_should_apply = models.TextField(blank=True)
    time_commitment = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
