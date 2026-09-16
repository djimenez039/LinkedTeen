import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import StudentProfile
from clubs.constants import CLUB_CHOICES, get_club_keywords
from clubs.models import Club


DEFAULT_FOCUS_AREAS = [
    'Computer engineering',
    'AI and accessibility',
    'Public speaking',
    'Leadership',
    'Social impact',
]

DEFAULT_OFFER = [
    'Python',
    'Canva',
    'Video editing',
    'Public speaking',
    'Event planning',
]

def _tokenize_keywords(value):
    if not value:
        return set()
    cleaned = re.split(r'[^a-zA-Z0-9]+', value.lower())
    return {token.strip() for token in cleaned if token and len(token) > 2}


def _match_reason(club_name, overlap):
    if overlap:
        return f"Your profile matches {club_name} because you listed {', '.join(overlap[:3])}."
    return f"This club is a strong fit for your interests, goals, and leadership profile."


@login_required
def dashboard(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if profile is None:
        profile = StudentProfile(user=request.user)

    full_name = (profile.full_name or '').strip()
    student_name = full_name.split()[0] if full_name else request.user.username

    student_keywords = set()
    for field_name in ['keywords', 'interests', 'skills', 'can_offer', 'causes', 'availability', 'club_interest', 'bio']:
        value = getattr(profile, field_name, '') or ''
        student_keywords.update(_tokenize_keywords(value))

    focus_areas = sorted(student_keywords)[:5] if student_keywords else DEFAULT_FOCUS_AREAS

    offer = (
        [item.strip() for item in (profile.can_offer or '').split(',') if item.strip()]
        if (profile.can_offer or '').strip()
        else DEFAULT_OFFER
    )
    ranked_clubs = []
    for club_name, _ in CLUB_CHOICES:
        club = Club.objects.filter(name=club_name).first()
        club_text = ' '.join([
            club_name,
            club.description if club else '',
            club.keywords if club else ', '.join(get_club_keywords(club_name)),
            club.needs if club else '',
            club.skills_needed if club else '',
        ])
        club_keyword_set = _tokenize_keywords(club_text)
        overlap = sorted(student_keywords.intersection(club_keyword_set))
        score = len(overlap)
        ranked_clubs.append({
            'title': club_name,
            'reason': _match_reason(club_name, overlap),
            'action': 'Explore this club',
            'score': score,
            'url': f'/clubs/{club.id}/' if club else '/clubs/',
        })

    ranked_clubs.sort(key=lambda item: (-item['score'], item['title']))
    matches = ranked_clubs[:3]

    context = {
        'student_name': student_name,
        'focus_areas': focus_areas,
        'offer': offer,
        'matches': matches,
        'opportunities': [],
    }
    return render(request, 'dashboards/dashboard.html', context)
