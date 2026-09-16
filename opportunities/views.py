from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Opportunity, OpportunityPost


def opportunities_index(request):
    query = request.GET.get('q', '').strip()
    opportunities = Opportunity.objects.all()
    if query:
        opportunities = opportunities.filter(title__icontains=query) | opportunities.filter(description__icontains=query)
    return render(request, 'opportunities/opportunities.html', {
        'opportunities': opportunities,
        'posts': OpportunityPost.objects.select_related('author')[:30],
        'query': query,
    })


@login_required
def create_post(request):
    if request.method == 'POST' and request.POST.get('body', '').strip():
        OpportunityPost.objects.create(author=request.user, body=request.POST['body'].strip())
        messages.success(request, 'Your opportunity update was shared.')
    return redirect('opportunities')
