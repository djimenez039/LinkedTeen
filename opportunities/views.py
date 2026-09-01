from django.shortcuts import render


def opportunities_index(request):
    opportunities = [
        {
            'title': 'STEM Leadership Summit',
            'category': 'Leadership',
            'description': 'A leadership and networking event for students exploring engineering, technology, and project leadership.',
            'skills_needed': 'Public speaking, teamwork, curiosity',
            'who_should_apply': 'Students interested in STEM and leadership.',
            'time_commitment': 'One weekend event',
        },
        {
            'title': 'Accessibility App Challenge',
            'category': 'Hackathon',
            'description': 'Students build an app or prototype focused on a real social problem.',
            'skills_needed': 'Python, design, product thinking, teamwork',
            'who_should_apply': 'Students passionate about technology and impact.',
            'time_commitment': '2-3 weeks',
        },
    ]
    return render(request, 'opportunities/opportunities.html', {'opportunities': opportunities})
