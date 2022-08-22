import locale
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from cliente.models import Cliente
from cliente.views import fill_navbar_style
from cuentas.models import Cuenta
from .models import Prestamo


@login_required()
def index(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        return new_loan(request)

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    user = request.user
    customer = Cliente.objects.get(user=user)
    max_loan = Prestamo.get_max_loan(customer)
    loan_types = []
    styles: dict = {}

    for loan_type in Prestamo.LoanType.choices:
        loan_types.append({'value': loan_type[0], 'label': loan_type[1]})

    context: dict = {'user': user,
                     'customer': customer,
                     'max_loan': max_loan,
                     'loan_currency': locale.currency(max_loan, grouping=True),
                     'loan_types': loan_types,
                     'styles': styles,
                     }
    template_name: str = 'prestamos/prestamos.html'

    fill_navbar_style(styles, customer)

    return render(request, template_name=template_name, context=context)


@login_required()
def new_loan(request: WSGIRequest) -> HttpResponse:
    # Retrieve User details
    user = request.user
    customer = Cliente.objects.get(user=user)

    # Create new Loan
    loan_type = request.POST['type']
    loan_amount = float(request.POST['amount'])

    if loan_amount > Prestamo.get_max_loan(customer):
        messages.error(request, 'Loan exceeds maximum amount')
        return redirect('loans')

    date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
    loan = Prestamo(customer=customer, type=loan_type, total=loan_amount, date=date)
    loan.save()

    # Update account balance
    account = Cuenta.objects.get(customer=user, type=Cuenta.AccountType.SAVINGS.value)
    account.balance += loan_amount
    account.save()

    messages.success(request, 'Loan granted.')

    return redirect('me')
