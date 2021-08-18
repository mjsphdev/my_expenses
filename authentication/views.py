from django.shortcuts import render, redirect
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.views import LoginView
# Create your views here.

class SignIn(LoginView):
    template_name = 'authentication/sign_in.html'
    redirect_authenticated_user = True
    success_url = '/dashboard/'

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect.')

    return render(request, 'authentication/sign_in.html')

def sign_out(request):
    logout(request)
    return redirect('sign_in')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
    
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user}')
    
                return redirect('sign_in')

    context = {'form': form}
    return render(request, 'authentication/sign_up.html', context)
 