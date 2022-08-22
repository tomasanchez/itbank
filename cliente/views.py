import locale

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from cuentas.models import Cuenta
from tarjetas.models import Tarjeta
from .models import Cliente


@login_required()
def index(request: WSGIRequest) -> HttpResponse:
    """
    View function for Me Page of site.
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    template_name: str = 'cliente/index.html'
    user = request.user
    costumer = Cliente.objects.get(user=user)
    main_account = Cuenta.objects.get(customer=user, type=Cuenta.AccountType.SAVINGS.value)
    credit_cards = Tarjeta.objects.filter(customer=user, type=Tarjeta.CardType.CREDIT.value)

    try:
        us_account = Cuenta.objects.get(customer=user, type=Cuenta.AccountType.SAVINGS_USD.value)
    except Cuenta.DoesNotExist:
        us_account = None

    navbar: str = "navbar-light bg-light"
    navbar_text: str = ""
    log_out: str = "text-dark"

    styles: dict = {
        "navbar": navbar,
        "navbar_text": navbar_text,
        "log_out": log_out,
        "account_balance": locale.currency(main_account.balance, grouping=True)
    }

    if us_account is not None:
        styles["us_balance"] = "US" + locale.currency(us_account.balance, grouping=True)
        styles["us_account"] = f"/ {us_account.iban}"

    context: dict = {
        "user": user,
        "costumer": costumer,
        "account": main_account,
        "styles": styles,
        'cards': credit_cards,
    }

    fill_navbar_style(styles, costumer)

    return render(request, template_name, context)


def fill_navbar_style(styles: dict = {}, customer: Cliente = None) -> dict:
    """
    Fill the navbar style with the customer's type.
    """
    styles['navbar'] = "navbar-light bg-body"
    styles['log_out'] = "text-dark"
    styles['cards_color'] = "bg-blueish"

    if customer is not None:
        if customer.type == Cliente.CustomerType.GOLD.value:
            styles['navbar'] = "navbar-light bg-gold"
            styles['navbar_text'] = "Premier"
            styles['cards_color'] = "bg-gold text-dark"
        elif customer.type == Cliente.CustomerType.BLACK.value:
            styles['navbar'] = "navbar-dark bg-prestigious"
            styles['navbar_text'] = "Prestigious"
            styles['log_out'] = "text-white"
            styles['cards_color'] = "bg-prestigious text-white"
            styles['card_svg'] = "svg-white"
            styles['card_text'] = "text-gray"
    return styles
