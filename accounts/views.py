from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from clubs.constants import CLUB_CHOICES
from .forms import CustomUserCreationForm
from .models import StudentProfile

INTEREST_OPTIONS = [
    'AI', 'Public speaking', 'Leadership', 'Engineering', 'Design', 'Social impact',
    'Technology', 'Research', 'Writing', 'Volunteering', 'Environment', 'Culture',
    'Music', 'Art', 'Sports', 'Health', 'Community service', 'Business', 'Finance', 'Law',
]
SKILL_OPTIONS = [
    'Python', 'Video editing', 'Canva', 'Leadership', 'Writing', 'Public speaking',
    'Event planning', 'Research', 'Design', 'Coding', 'Marketing', 'Photography', 'Data analysis',
]
OFFER_OPTIONS = [
    'Python', 'Public speaking', 'Event planning', 'Canva', 'Video editing', 'Leadership',
    'Research', 'Design', 'Writing', 'Mentorship', 'Project planning',
]
LOOKING_FOR_OPTIONS = [
    'AI projects', 'Engineering mentor', 'Leadership role', 'Research experience',
    'Mentorship', 'Design feedback', 'Public speaking opportunities', 'Community project',
    'Students building social impact projects', 'Startup ideas', 'Career exploration',
]
GOAL_OPTIONS = [
    'Build projects', 'Gain leadership experience', 'Explore engineering', 'Find mentors',
    'Develop public speaking', 'Create social impact', 'Learn new tools', 'Career exploration',
]
AVAILABILITY_OPTIONS = [
    '2-4 hours per week', 'Weekends', 'Afternoons', 'School year only', 'Summer only', 'Evenings',
]

PROFILE_OPTION_SETS = {
    'interests': INTEREST_OPTIONS,
    'skills': SKILL_OPTIONS,
    'can_offer': OFFER_OPTIONS,
    'looking_for': LOOKING_FOR_OPTIONS,
    'goals': GOAL_OPTIONS,
    'availability': AVAILABILITY_OPTIONS,
}


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('accounts:onboarding')

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required
def onboarding_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.grade = request.POST.get('grade', profile.grade)
        profile.school = request.POST.get('school', profile.school)
        profile.bio = request.POST.get('bio', profile.bio)
        for field_name, options in PROFILE_OPTION_SETS.items():
            values = request.POST.getlist(field_name)
            if values:
                setattr(profile, field_name, ', '.join(values))
            else:
                setattr(profile, field_name, '')
        profile.club_interest = ', '.join(request.POST.getlist('club_interest'))
        profile.save()
        return redirect('dashboard')

    context = {'profile': profile, 'club_choices': CLUB_CHOICES}
    for key, value in PROFILE_OPTION_SETS.items():
        context[f'{key}_options'] = value
    return render(request, 'accounts/onboarding.html', context)


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})
