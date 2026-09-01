from django.shortcuts import render


def clubs_index(request):
    clubs = [
        {
            'name': 'Robotics Club',
            'description': 'Students building tech projects and participating in competitions.',
            'needs': 'Python programmer, event organizer, outreach lead',
            'skills_needed': 'Python, CAD, presentation, testing',
            'time_commitment': '2-3 hours per week',
        },
        {
            'name': 'Lift Up Club',
            'description': 'Community-focused student group creating impact through media, volunteering, and events.',
            'needs': 'Video editor, social media support, fundraiser help',
            'skills_needed': 'Canva, video editing, storytelling, photography',
            'time_commitment': '1-2 hours per week',
        },
    ]
    return render(request, 'clubs/clubs.html', {'clubs': clubs})
