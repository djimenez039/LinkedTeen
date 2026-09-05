from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import StudentProfile


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
        profile.interests = request.POST.get('interests', profile.interests)
        profile.skills = request.POST.get('skills', profile.skills)
        profile.can_offer = request.POST.get('can_offer', profile.can_offer)
        profile.looking_for = request.POST.get('looking_for', profile.looking_for)
        profile.goals = request.POST.get('goals', profile.goals)
        profile.causes = request.POST.get('causes', profile.causes)
        profile.availability = request.POST.get('availability', profile.availability)
        profile.save()
        return redirect('dashboard')

    return render(request, 'accounts/onboarding.html', {'profile': profile})


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})
