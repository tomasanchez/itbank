from django.contrib.auth import authenticate, login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

from cliente.models import Cliente
# Create your views here.
from .forms import RegisterForm


def index(request: WSGIRequest) -> HttpResponse:
    """
    View function for Login Page of site.
    """
    if request.user.is_authenticated:
        return redirect('me')

    template_name: str = 'login/index.html'
    context: dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                Cliente.objects.get(user=user)
                nxt = request.GET.get("next", 'me')
                login(request, user)
                return redirect(nxt)
            except Cliente.DoesNotExist:
                context['error'] = 'User not authorized'
        else:
            context['error'] = 'Invalid username or password'

    return render(request, template_name, context)


def log_out(request: WSGIRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


def reset(request: WSGIRequest) -> HttpResponse:
    """
    View function for Reset Password Page of site.
    """
    template_name: str = 'login/reset.html'
    context: dict = {}
    return render(request, template_name, context)


def register(request: WSGIRequest) -> HttpResponse:
    """
    View function for Register Page of site.
    """
    template_name: str = 'login/register.html'
    form: RegisterForm = RegisterForm()
    context: dict = {'form': form}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save_customer()
            return redirect('login')

    return render(request, template_name, context)
