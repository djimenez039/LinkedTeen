from django.shortcuts import render
from django.urls import reverse
from urllib.parse import urlencode

from clubs.constants import CLUB_CHOICES
from clubs.models import Club


HOME_CLUB_NAMES = ('Chess Club', 'DECA', 'Beaches Go Green')
GENERATED_CLUB_DESCRIPTION = 'A student-led club focused on leadership, service, creativity, or community impact.'

def home(request):
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard')
    catalog_names = {name for name, _ in CLUB_CHOICES}
    clubs_by_name = {club.name: club for club in Club.objects.filter(name__in=HOME_CLUB_NAMES)}
    preview_clubs = []
    for name in HOME_CLUB_NAMES:
        if name not in catalog_names:
            continue
        club = clubs_by_name.get(name)
        preview_clubs.append({
            'name': name,
            'description': club.description if club and club.description != GENERATED_CLUB_DESCRIPTION else '',
            'url': reverse('club_detail', args=[club.pk]) if club else f"{reverse('clubs')}?{urlencode({'q': name})}",
        })

    return render(request, 'home.html', {'preview_clubs': preview_clubs})

# Create your views here.
