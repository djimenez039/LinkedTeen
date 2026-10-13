from django.shortcuts import render
from clubs.models import Club

def home(request):
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard')
    return render(request, 'home.html', {'club_count': Club.objects.count()})


def terms(request):
    return render(request, 'legal/terms.html')


def privacy(request):
    return render(request, 'legal/privacy.html')

# Create your views here.
