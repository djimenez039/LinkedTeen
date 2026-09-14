import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import StudentProfile
from clubs.constants import CLUB_CHOICES


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

DEFAULT_LOOKING_FOR = [
    'AI projects',
    'Engineering mentor',
    'Leadership role',
    'Research experience',
    'Students building social impact projects',
]


def _tokenize_keywords(value):
    if not value:
        return set()
    cleaned = re.split(r'[^a-zA-Z0-9]+', value.lower())
    return {token.strip() for token in cleaned if token and len(token) > 2}


def _club_tokens(club_name):
    tokens = set()
    for part in re.split(r'[^a-zA-Z0-9]+', club_name.lower()):
        if part and len(part) > 2:
            tokens.add(part)
    return tokens


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
    for field_name in [
        'keywords', 'interests', 'skills', 'can_offer', 'looking_for', 'goals', 'causes', 'club_interest'
    ]:
        value = getattr(profile, field_name, '') or ''
        student_keywords.update(_tokenize_keywords(value))

    focus_areas = sorted(student_keywords)[:5] if student_keywords else DEFAULT_FOCUS_AREAS

    offer = (
        [item.strip() for item in (profile.can_offer or '').split(',') if item.strip()]
        if (profile.can_offer or '').strip()
        else DEFAULT_OFFER
    )
    looking_for = (
        [item.strip() for item in (profile.looking_for or '').split(',') if item.strip()]
        if (profile.looking_for or '').strip()
        else DEFAULT_LOOKING_FOR
    )

    ranked_clubs = []
    for club_name, _ in CLUB_CHOICES:
        club_keyword_set = _club_tokens(club_name)
        overlap = sorted(student_keywords.intersection(club_keyword_set))
        score = len(overlap)
        ranked_clubs.append({
            'title': club_name,
            'reason': _match_reason(club_name, overlap),
            'action': 'Explore this club',
            'score': score,
        })

    ranked_clubs.sort(key=lambda item: (-item['score'], item['title']))
    matches = ranked_clubs[:3]

    context = {
        'student_name': student_name,
        'focus_areas': focus_areas,
        'offer': offer,
        'looking_for': looking_for,
        'matches': matches,
        'opportunities': [
            'Robotics competition recruiting teams',
            'Student podcast collaboration',
            'Community engineering mentor session',
            'Accessibility app hackathon',
        ],
    }
    return render(request, 'dashboards/dashboard.html', context)
