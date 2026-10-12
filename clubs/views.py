from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .constants import CLUB_CHOICES, PRESIDENT_ROSTER, get_club_keywords
from .models import Club, ClubAnnouncement, ClubMembership


def _get_membership(club, user):
    if not user.is_authenticated:
        return None
    return ClubMembership.objects.filter(club=club, student=user).first()


def _can_manage_announcements(club, user, membership):
    return user.is_authenticated and (
        user.is_staff
        or club.created_by_id == user.pk
        or (membership and membership.role in {'leader', 'sponsor'})
    )


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
    membership = _get_membership(club, request.user)
    is_member = membership is not None
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'membership': membership,
        'is_member': is_member,
        'can_manage_announcements': _can_manage_announcements(club, request.user, membership),
        'announcements': club.announcements.select_related('author')[:30],
        'posts': club.posts.select_related('author')[:30] if is_member else [],
    })


@login_required
def create_club_post(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if _get_membership(club, request.user) is None:
        messages.error(request, 'Join this club before posting to its group.')
        return redirect('club_detail', club_id=club.id)
    if request.method == 'POST' and request.POST.get('body', '').strip():
        club.posts.create(author=request.user, body=request.POST['body'].strip())
        messages.success(request, 'Your post was added to the club group.')
    return redirect('club_detail', club_id=club.id)


@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        _, created = ClubMembership.objects.get_or_create(club=club, student=request.user)
        if created:
            messages.success(request, f'You are now a member of {club.name}.')
        else:
            messages.info(request, f'You are already a member of {club.name}.')
    return redirect('club_detail', club_id=club.id)


@login_required
def create_club_announcement(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    membership = _get_membership(club, request.user)
    if not _can_manage_announcements(club, request.user, membership):
        raise PermissionDenied
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        if title and body:
            ClubAnnouncement.objects.create(club=club, author=request.user, title=title, body=body)
            messages.success(request, 'Your announcement was published.')
        else:
            messages.error(request, 'Add both a title and announcement text.')
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
