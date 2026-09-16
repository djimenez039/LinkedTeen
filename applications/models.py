from django.db import models
from django.conf import settings


class ClubApplication(models.Model):
	club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name='applications')
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_applications')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['club', 'student'], name='unique_club_application'),
		]

# Create your models here.
