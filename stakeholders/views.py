from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    return render(request, 'stakeholders/index.html', {})

def home(request):
    login_failed = request.GET.get('login_failed', False)
    register_failed = request.GET.get('register_failed', False)
    
    context = {
        'login_failed': login_failed,
        'register_failed': register_failed,
    }
    
    return render(request, 'stakeholders/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('home')
        else:
            # Invalid login
            error_message = "Ocorreu um erro."
            return render(request, 'stakeholders/home.html', {'error_message': error_message})
    
    # Render the login page
    return render(request, 'stakeholders/home.html')


def logout_view(request):
    logout(request)
    # Redirect to a success page or homepage
    return redirect('home')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect(reverse('home') + '?register_failed=True')

        # Check if a user with the same username or email already exists
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect(reverse('home') + '?register_failed=True')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect(reverse('home') + '?register_failed=True')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        
        # Registration successful, redirect to home without an error message
        return redirect(reverse('home'))
    else:
        # Render the home template with an empty form
        return render(request, 'home.html')



