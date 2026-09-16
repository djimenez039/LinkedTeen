from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from clubs.constants import CLUB_CHOICES
from .forms import CustomUserCreationForm, EmailOrUsernameAuthenticationForm
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
AVAILABILITY_OPTIONS = [
    '2-4 hours per week', 'Weekends', 'Afternoons', 'School year only', 'Summer only', 'Evenings',
]

PROFILE_OPTION_SETS = {
    'interests': INTEREST_OPTIONS,
    'skills': SKILL_OPTIONS,
    'availability': AVAILABILITY_OPTIONS,
}


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = EmailOrUsernameAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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

    context = {'profile': profile, 'club_choices': CLUB_CHOICES, 'grade_choices': StudentProfile.GRADE_CHOICES}
    for key, value in PROFILE_OPTION_SETS.items():
        context[f'{key}_options'] = value
        context[f'{key}_selected'] = [item.strip() for item in getattr(profile, key).split(',') if item.strip()]
    context['club_interest_selected'] = [item.strip() for item in profile.club_interest.split(',') if item.strip()]
    return render(request, 'accounts/onboarding.html', context)


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def settings_view(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username', request.user.username).strip()
        request.user.email = request.POST.get('email', request.user.email).strip()
        if request.user.is_staff:
            request.user.role = request.POST.get('role', request.user.role)
        request.user.save(update_fields=['username', 'email', 'role'])
        messages.success(request, 'Your account settings were updated.')
        return redirect('accounts:settings')
    return render(request, 'accounts/settings.html', {'role_choices': request.user.ROLE_CHOICES})
