from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import LoginForm, SignupForm, ProfileForm

def login_view(request):
    error = None
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=None, require_https=request.is_secure()):
                    return redirect(next_url)
                return redirect('questions:index')
            else:
                error = 'Invalid login or password'
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form, 'error': error, 'next': next_url})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('questions:index')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile_view(request):
    success = None
    error = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            success = 'Profile updated successfully!'
        else:
            error = 'Please correct the errors below.'
    else:
        form = ProfileForm(instance=request.user.profile, user=request.user)
    return render(request, 'core/profile.html', {
        'form': form,
        'success': success,
        'error': error
    })

def logout_view(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('questions:index')
