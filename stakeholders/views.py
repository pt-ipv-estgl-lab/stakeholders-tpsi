from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AtividadeFormativa, EventoCientifico, Servico, Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def index(request):
    return render(request, 'stakeholders/index.html', {})

def home(request):
    login_failed = request.GET.get('login_failed', False)
    register_failed = request.GET.get('register_failed', False)
    servicos = Servico.objects.all()
    cursos = AtividadeFormativa.objects.filter(tipodeatividade='C')
    formacoes = AtividadeFormativa.objects.filter(tipodeatividade='F')
    congressos = EventoCientifico.objects.filter(tipodeevento='CO')
    concursos = EventoCientifico.objects.filter(tipodeevento='CN')
    palestras = EventoCientifico.objects.filter(tipodeevento='PA')
    seminarios = EventoCientifico.objects.filter(tipodeevento='SE')
    
    context = {
        'login_failed': login_failed,
        'register_failed': register_failed,
        'cursos': cursos,
        'formacoes': formacoes,
        'congressos': congressos,
        'concursos' : concursos,
        'palestras' : palestras,
        'seminarios' : seminarios,
        'servicos' : servicos,
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

        # Create a profile for the user with all fields blank
        profile = Profile.objects.create(user=user, nome_completo='', nif='', morada='',
                                         codigo_postal='', freguesia='', concelho='',
                                         distrito='', contacto='')

        # Log in the user
        login(request, user)

        # Registration successful, redirect to home without an error message
        return redirect(reverse('home'))
    else:
        # Render the home template with an empty form
        return render(request, 'home.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Process the form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # ... process other form fields

        # Update the user profile or perform other actions

        # Redirect to a different page after processing the form
        return redirect('profile')  # Assuming 'profile' is the name of the URL pattern for the profile view

    # Load the current logged-in user's information
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email

    # Access the additional fields from the user profile model
    profile = user.profile  # Assuming the user profile is related to the User model via a one-to-one field

    nome_completo = profile.nome_completo
    nif = profile.nif
    morada = profile.morada
    codigo_postal = profile.codigo_postal
    freguesia = profile.freguesia
    concelho = profile.concelho
    distrito = profile.distrito
    contacto = profile.contacto

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'nome_completo': nome_completo,
        'nif': nif,
        'morada': morada,
        'codigo_postal': codigo_postal,
        'freguesia': freguesia,
        'concelho': concelho,
        'distrito': distrito,
        'contacto': contacto,
    }

    return render(request, 'stakeholders/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile  # Assuming you have a OneToOne relationship between User and Profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view after successful submission
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'stakeholders/profile.html', {'form': form})



