from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from cliente.models import Cliente
from cliente.views import fill_navbar_style
from .models import Cuenta


@login_required()
def index(request):
    user: User = request.user
    customer: Cliente = Cliente.objects.get(user=user)
    styles: dict = {}
    fill_navbar_style(styles, customer=customer)
    accounts: Cuenta = Cuenta.objects.filter(customer=user)
    context: dict = {"styles": styles, "accounts": accounts}
    return render(request, 'cuentas/index.html', context)
