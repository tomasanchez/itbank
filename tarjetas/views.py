from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from cliente.models import Cliente
from cliente.views import fill_navbar_style
from .models import Tarjeta


@login_required()
def my_cards(request: WSGIRequest) -> HttpResponse:
    customer = Cliente.objects.get(user=request.user)
    cards = Tarjeta.objects.filter(customer=customer.user)
    context: dict = {}
    styles: dict = {}
    fill_navbar_style(styles, customer)
    context["styles"] = styles
    context["cards"] = cards
    return render(request, 'tarjetas/my_cards.html', context=context)
