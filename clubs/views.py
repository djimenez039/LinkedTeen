from django.shortcuts import render

from .constants import CLUB_CHOICES


def clubs_index(request):
    clubs = []
    for name, _ in CLUB_CHOICES:
        clubs.append({
            'name': name,
            'description': 'A student-led club focused on leadership, service, creativity, or community impact.',
            'needs': 'Student members, collaboration, event support, and leadership.',
            'skills_needed': 'Communication, teamwork, project planning, and initiative.',
            'time_commitment': '1-3 hours per week',
        })
    return render(request, 'clubs/clubs.html', {'clubs': clubs[:20]})
