from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def login_view(request):
	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		return redirect('home')

	return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
	form = UserCreationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user)
		return redirect('home')

	return render(request, 'accounts/register.html', {'form': form})
