from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import *
from .models import *

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomLogoutForm

def custom_logout_view(request):
    if request.method == 'POST':
        form = CustomLogoutForm(request.POST)
        if form.is_valid():
            logout(request)
            return redirect(reverse('home'))
    else:
        form = CustomLogoutForm()
    return render(request, 'accounts/logout.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})


