from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    profile = getattr(request.user, 'student_profile', None)
    student_name = profile.full_name.split()[0] if profile and profile.full_name else request.user.username

    context = {
        'student_name': student_name,
        'focus_areas': [
            'Computer engineering',
            'AI and accessibility',
            'Public speaking',
            'Leadership',
            'Social impact',
        ],
        'offer': (
            profile.can_offer.split(',') if profile and profile.can_offer else [
                'Python',
                'Canva',
                'Video editing',
                'Public speaking',
                'Event planning',
            ]
        ),
        'looking_for': (
            profile.looking_for.split(',') if profile and profile.looking_for else [
                'AI projects',
                'Engineering mentor',
                'Leadership role',
                'Research experience',
                'Students building social impact projects',
            ]
        ),
        'matches': [
            {
                'title': 'Robotics Club',
                'reason': 'You both want to build tech projects with social impact.',
                'action': 'Connect about a team project',
            },
            {
                'title': 'Maya Chen',
                'reason': 'She is looking for a programming partner and you listed Python.',
                'action': 'Ask about collaboration',
            },
            {
                'title': 'Lift Up Club',
                'reason': 'Lift Up needs a video editor and social media support.',
                'action': 'Apply for a role',
            },
        ],
        'opportunities': [
            'Robotics competition recruiting teams',
            'Student podcast collaboration',
            'Community engineering mentor session',
            'Accessibility app hackathon',
        ],
    }
    return render(request, 'dashboards/dashboard.html', context)
