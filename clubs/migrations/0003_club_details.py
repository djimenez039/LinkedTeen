from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('clubs', '0002_club_keywords')]

    operations = [
        migrations.AddField(model_name='club', name='availability', field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(model_name='club', name='presidents', field=models.CharField(blank=True, help_text='Separate multiple presidents with commas.', max_length=255)),
        migrations.AddField(model_name='club', name='sponsor', field=models.CharField(blank=True, max_length=150)),
    ]