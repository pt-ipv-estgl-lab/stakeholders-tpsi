from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Entidade, Servico, Participante, PreInscricao, Evento, Oferta
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'stakeholders/index.html', {})

def home(request):
    login_failed = request.GET.get('login_failed', False)
    register_failed = request.GET.get('register_failed', False)
    servicos = Servico.objects.all()
    cursos = Evento.objects.filter(tipoevento='C')
    formacoes = Evento.objects.filter(tipoevento='F')
    congressos = Evento.objects.filter(tipoevento='CO')
    concursos = Evento.objects.filter(tipoevento='CN')
    palestras = Evento.objects.filter(tipoevento='PA')
    seminarios = Evento.objects.filter(tipoevento='SE')
    
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
        participante = Participante.objects.create(user=user, nomes_do_meio='', nif='', morada='',
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

        if user.participante.nomes_do_meio != request.POST.get('nomes_do_meio'):
            user.participante.nomes_do_meio = request.POST.get('nomes_do_meio')
            updated_fields.append('Nome Completo')

        if user.participante.nif != request.POST.get('nif'):
            user.participante.nif = request.POST.get('nif')
            updated_fields.append('Nif')

        if user.participante.morada != request.POST.get('morada'):
            user.participante.morada = request.POST.get('morada')
            updated_fields.append('Morada')

        if user.participante.codigo_postal != request.POST.get('codigo_postal'):
            user.participante.codigo_postal = request.POST.get('codigo_postal')
            updated_fields.append('Código Postal')

        if user.participante.freguesia != request.POST.get('freguesia'):
            user.participante.freguesia = request.POST.get('freguesia')
            updated_fields.append('Freguesia')

        if user.participante.concelho != request.POST.get('concelho'):
            user.participante.concelho = request.POST.get('concelho')
            updated_fields.append('Concelho')

        if user.participante.distrito != request.POST.get('distrito'):
            user.participante.distrito = request.POST.get('distrito')
            updated_fields.append('Distrito')

        if user.participante.contacto != request.POST.get('contacto'):
            user.participante.contacto = request.POST.get('contacto')
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
        user.participante.save()

        # Redirect to a different page after processing the form
        return redirect('profile')  # Assuming 'profile' is the name of the URL pattern for the profile view
    
    
    # Load the current logged-in user's information
    user = request.user
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email

    # Access the additional fields from the user profile model
    participante = user.participante

    nomes_do_meio = participante.nomes_do_meio
    nif = participante.nif
    morada = participante.morada
    codigo_postal = participante.codigo_postal
    freguesia = participante.freguesia
    concelho = participante.concelho
    distrito = participante.distrito
    contacto = participante.contacto

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'nomes_do_meio': nomes_do_meio,
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
        user.participante.nomes_do_meio = request.POST.get('nomes_do_meio')
        user.participante.nif = request.POST.get('nif')
        user.participante.morada = request.POST.get('morada')
        user.participante.codigo_postal = request.POST.get('codigo_postal')
        user.participante.freguesia = request.POST.get('freguesia')
        user.participante.concelho = request.POST.get('concelho')
        user.participante.distrito = request.POST.get('distrito')
        user.participante.contacto = request.POST.get('contacto')

        user.save()
        user.participante.save()

        # Check if the user is already registered for the activity
        existing_inscricao = PreInscricao.objects.filter(participante_id=user.participante.id, atividade_id=request.POST.get('idatividade1')).first()
        if existing_inscricao:
            messages.error(request, 'Já está inscrito nesta atividade.')
            return redirect('home')  # Redirect to home or display an error message

        inscricao = PreInscricao.objects.create(participante_id=user.participante.id, atividade_id=request.POST.get('idatividade1'))
        messages.success(request, 'Pré-Inscrição efetuada com sucesso!')

        return redirect('home')  # Replace 'home' with the desired URL or URL pattern name

    return render(request, 'stakeholders/home.html')

def logininscricao_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Update the session to reflect the logged-in user
            request.session.modified = True
            # Return success response
            return JsonResponse({'success': True})
        else:
            # Invalid login
            return JsonResponse({'success': False})
    
    # Return error response for non-POST requests
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def inscricaoregisto_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first = request.POST.get('first_name')
        last = request.POST.get('last_name')

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
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first, last_name=last)

        # Create a profile for the user with all fields blank
        participante = Participante.objects.create(user=user, nomes_do_meio=request.POST.get('nomes_do_meio'), nif=request.POST.get('nif'), morada=request.POST.get('morada'),
                                         codigo_postal=request.POST.get('codigo_postal'), freguesia= request.POST.get('freguesia'), concelho=request.POST.get('concelho'),
                                         distrito=request.POST.get('distrito'), contacto=request.POST.get('contacto'))

        # Log in the user
        login(request, user)
        
        existing_inscricao = PreInscricao.objects.filter(participante_id=participante.id, atividade_id=request.POST.get('idatividade')).first()
        if existing_inscricao:
            messages.error(request, 'Já está inscrito nesta atividade.')
            return redirect('home')  # Redirect to home or display an error message

        inscricao = PreInscricao.objects.create(participante_id=user.participante.id, atividade_id=request.POST.get('idatividade'))
        messages.success(request, 'Pré-Inscrição efetuada com sucesso!')

        # Registration successful, redirect to home without an error message
        return redirect(reverse('home'))
    else:
        # Render the home template with an empty form
        return render(request, 'home.html')



def requisitar_view(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse nome de utilizador já existe.')
            return redirect('requisitar')  # Replace 'requisitar' with the URL name of your error page

        try:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Log in the user
            auth_user = authenticate(request, username=username, password=password)
            if auth_user:
                login(request, auth_user)
            else:
                messages.error(request, 'Não foi possível realizar o login.')
                return redirect('requisitar')  # Replace 'requisitar' with the URL name of your error page
        except Exception:
            messages.error(request, 'Ocorreu um erro com o seu pedido, por favor volte a tentar')
            return redirect('requisitar')  # Replace 'requisitar' with the URL name of your error page


        # Create a profile for the user with all fields blank
        participante = Participante.objects.create(user=user, nomes_do_meio='', nif='', morada='',
                                         codigo_postal='', freguesia='', concelho='',
                                         distrito='', contacto='',data_nascimento=date.today())
        
        
        # Create new oferta
        nome_empresa = request.POST.get('nome_empresa')
        morada = request.POST.get('morada')
        codigo_postal = request.POST.get('codigo_postal')
        contacto_telefonico = request.POST.get('contacto_telefonico')
        entidade_id = request.POST.get('entidade_id')
        descricao = request.POST.get('descricao')

        oferta = Oferta(
            nome_empresa=nome_empresa,
            morada=morada,
            codigo_postal=codigo_postal,
            contacto_telefonico=contacto_telefonico,
            email=email,
            entidade_id=entidade_id,
            descricao=descricao,
            user=user
        )
        oferta.save()

        messages.success(request, 'Requisição Enviada com Sucesso')
        return redirect('requisitar')  # Replace 'requisitar' with the URL name of your success page

    # Get all Entidade objects
    entidades = Entidade.objects.all()

    context = {
        'entidades': entidades
    }

    return render(request, 'stakeholders/requisitar.html', context)