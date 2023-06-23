from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AtividadeFormativa, EventoCientifico, Servico, Profile, Atividade, Inscricao
from django.contrib.auth.decorators import login_required


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
        # Update the user profile or perform other actions
        user = request.user
        # ... update other user fields
        updated_fields = []

        if user.first_name != request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            updated_fields.append('Primeiro Nome')

        if user.last_name != request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
            updated_fields.append('Último Nome')

        if user.profile.nome_completo != request.POST.get('nome_completo'):
            user.profile.nome_completo = request.POST.get('nome_completo')
            updated_fields.append('Nome Completo')

        if user.profile.nif != request.POST.get('nif'):
            user.profile.nif = request.POST.get('nif')
            updated_fields.append('Nif')

        if user.profile.morada != request.POST.get('morada'):
            user.profile.morada = request.POST.get('morada')
            updated_fields.append('Morada')

        if user.profile.codigo_postal != request.POST.get('codigo_postal'):
            user.profile.codigo_postal = request.POST.get('codigo_postal')
            updated_fields.append('Código Postal')

        if user.profile.freguesia != request.POST.get('freguesia'):
            user.profile.freguesia = request.POST.get('freguesia')
            updated_fields.append('Freguesia')

        if user.profile.concelho != request.POST.get('concelho'):
            user.profile.concelho = request.POST.get('concelho')
            updated_fields.append('Concelho')

        if user.profile.distrito != request.POST.get('distrito'):
            user.profile.distrito = request.POST.get('distrito')
            updated_fields.append('Distrito')

        if user.profile.contacto != request.POST.get('contacto'):
            user.profile.contacto = request.POST.get('contacto')
            updated_fields.append('Contacto')

        # Change password
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password or confirm_password:  # Check if any of the password fields are not empty
            if new_password == confirm_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    updated_fields.append('Password')
                    user.save()

                    # Re-authenticate the user with the new password
                    updated_user = authenticate(request, username=user.username, password=new_password)
                    if updated_user is not None:
                        login(request, updated_user)
                    else:
                        messages.error(request, 'Falha ao efetuar o login após a alteração da password.')
                else:
                    messages.error(request, 'A password antiga não corresponde.')
            else:
                messages.error(request, 'A nova password e a confirmação não correspondem.')

        if updated_fields:
            # Set a success message with the updated fields
            success_message = f"Mudanças efetuadas nos campos: {', '.join(updated_fields)}"
            messages.success(request, success_message)
            
        # Save the changes to the user and profile models
        user.save()
        user.profile.save()

        # Redirect to a different page after processing the form
        return redirect('profile')  # Assuming 'profile' is the name of the URL pattern for the profile view
    
    
    # Load the current logged-in user's information
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email

    # Access the additional fields from the user profile model
    profile = user.profile

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
def inscricao_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        # Update the profile fields with the submitted form data
        user.profile.nome_completo = request.POST.get('nome_completo')
        user.profile.nif = request.POST.get('nif')
        user.profile.morada = request.POST.get('morada')
        user.profile.codigo_postal = request.POST.get('codigo_postal')
        user.profile.freguesia = request.POST.get('freguesia')
        user.profile.concelho = request.POST.get('concelho')
        user.profile.distrito = request.POST.get('distrito')
        user.profile.contacto = request.POST.get('contacto')

        user.save()
        user.profile.save()

        # Check if the user is already registered for the activity
        existing_inscricao = Inscricao.objects.filter(profile=user.profile, atividade_id=request.POST.get('idatividade')).first()
        if existing_inscricao:
            messages.error(request, 'Já está inscrito nesta atividade.')
            return redirect('home')  # Redirect to home or display an error message

        inscricao = Inscricao.objects.create(profile_id=user.profile.id, atividade_id=request.POST.get('idatividade'))
        messages.success(request, 'Pré-Inscrição efetuada com sucesso!')

        return redirect('home')  # Replace 'home' with the desired URL or URL pattern name

    return render(request, 'stakeholders/home.html')





