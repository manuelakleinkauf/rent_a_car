from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserCreateForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list_vehicles')  # ajuste para a sua URL
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
    else:
        form = UserCreateForm()

    return render(request, 'login/create_user.html', {'form': form})