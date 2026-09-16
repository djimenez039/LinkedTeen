from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .constants import CLUB_CHOICES, PRESIDENT_ROSTER, get_club_keywords
from .models import Club
from applications.models import ClubApplication


def _get_or_create_club(name):
    club_index = next(index for index, (club_name, _) in enumerate(CLUB_CHOICES) if club_name == name)
    president = PRESIDENT_ROSTER[club_index] if club_index < len(PRESIDENT_ROSTER) else 'Student leadership team'
    club, _ = Club.objects.get_or_create(
        name=name,
        defaults={
            'description': 'A student-led club focused on leadership, service, creativity, or community impact.',
            'needs': 'Student members, collaboration, event support, and leadership.',
            'skills_needed': 'Communication, teamwork, project planning, and initiative.',
            'time_commitment': '1-3 hours per week',
            'availability': 'Weekdays and weekends',
            'keywords': ', '.join(get_club_keywords(name)),
            'presidents': president,
        },
    )
    if not club.presidents:
        club.presidents = president
        club.save(update_fields=['presidents'])
    return club


def clubs_index(request):
    query = request.GET.get('q', '').strip()
    interest = request.GET.get('interest', '').strip()
    clubs = [_get_or_create_club(name) for name, _ in CLUB_CHOICES]
    if query:
        clubs = [club for club in clubs if query.lower() in f'{club.name} {club.description} {club.keywords}'.lower()]
    if interest:
        clubs = [club for club in clubs if interest.lower() in f'{club.name} {club.description} {club.keywords}'.lower()]
    for club in clubs:
        club.keyword_list = [item.strip() for item in club.keywords.split(',') if item.strip()]
    return render(request, 'clubs/clubs.html', {
        'clubs': clubs,
        'query': query,
        'interest': interest,
        'interest_options': sorted({keyword.strip() for name, _ in CLUB_CHOICES for keyword in get_club_keywords(name)}),
    })


def club_detail(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not club.presidents and club.name in dict(CLUB_CHOICES):
        club = _get_or_create_club(club.name)
    application = None
    if request.user.is_authenticated:
        application = ClubApplication.objects.filter(club=club, student=request.user).first()
    return render(request, 'clubs/club_detail.html', {'club': club, 'application': application, 'posts': club.posts.select_related('author')[:30]})


@login_required
def create_club_post(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST' and request.POST.get('body', '').strip():
        club.posts.create(author=request.user, body=request.POST['body'].strip())
        messages.success(request, 'Your post was added to the club group.')
    return redirect('club_detail', club_id=club.id)


@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        _, created = ClubApplication.objects.get_or_create(club=club, student=request.user)
        if created:
            messages.success(request, f'Your request to join {club.name} was submitted.')
        else:
            messages.info(request, f'You already requested to join {club.name}.')
    return redirect('club_detail', club_id=club.id)


@login_required
def edit_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not (request.user.is_staff or request.user.role in {'faculty', 'organization'} or club.created_by == request.user):
        messages.error(request, 'You do not have permission to edit this club.')
        return redirect('club_detail', club_id=club.id)
    if request.method == 'POST':
        for field in ('description', 'needs', 'skills_needed', 'time_commitment', 'availability', 'presidents', 'sponsor', 'keywords'):
            setattr(club, field, request.POST.get(field, '').strip())
        club.save()
        messages.success(request, 'Club details updated.')
        return redirect('club_detail', club_id=club.id)
    return render(request, 'clubs/club_edit.html', {'club': club})
