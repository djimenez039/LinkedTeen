from django.conf import settings
from django.db import migrations, models
from django.db.migrations import swappable_dependency
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [swappable_dependency(settings.AUTH_USER_MODEL), ('clubs', '0003_club_details')]
    operations = [
        migrations.CreateModel(
            name='ClubApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='clubs.club')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'constraints': [models.UniqueConstraint(fields=('club', 'student'), name='unique_club_application')]},
        ),
    ]