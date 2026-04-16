from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

def login_view(request):
    error = None
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        # Здесь будет проверка в БД
        if login == 'dr_pepper' and password == 'password':
            return redirect('questions:index')
        else:
            error = 'Invalid login or password'
    
    return render(request, 'core/login.html', {'error': error})

def signup_view(request):
    error = None
    if request.method == 'POST':
        login = request.POST.get('login')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Валидация
        if not login or not email or not nickname or not password:
            error = 'All fields are required'
        elif password != password2:
            error = 'Passwords do not match'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters'
        else:
            # Здесь будет создание пользователя в БД
            return redirect('core:login')
    
    return render(request, 'core/signup.html', {'error': error})

def profile_view(request):
    success = None
    error = None
    form_errors = {}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Валидация
        if not email:
            form_errors['email'] = 'Email is required'
        elif '@' not in email:
            form_errors['email'] = 'Invalid email address'
            
        if not nickname:
            form_errors['nickname'] = 'Nickname is required'
            
        # Проверка пароля если меняют
        if new_password:
            if not current_password:
                error = 'Current password is required to change password'
            elif len(new_password) < 6:
                error = 'New password must be at least 6 characters'
            elif new_password != confirm_password:
                error = 'New passwords do not match'
            else:
                success = 'Profile updated successfully! Password has been changed.'
        elif not error:
            success = 'Profile updated successfully!'
    
    return render(request, 'core/profile.html', {
        'success': success,
        'error': error,
        'form_errors': form_errors
    })

def logout_view(request):
    auth_logout(request)
    return redirect('questions:index')
