from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from cliente.models import Cliente
from cliente.views import fill_navbar_style
from .models import Cuenta, Transaction


@login_required()
def index(request):
    user: User = request.user
    customer: Cliente = Cliente.objects.get(user=user)
    styles: dict = {}
    fill_navbar_style(styles, customer=customer)
    accounts: Cuenta = Cuenta.objects.filter(customer=user)
    context: dict = {"styles": styles, "accounts": accounts}
    return render(request, 'cuentas/index.html', context)


@login_required()
def details_page(request, pk):
    user: User = request.user
    context: dict = {}

    try:
        account: Cuenta = Cuenta.objects.get(pk=pk, customer=user)
        context["account"] = account
        transactions: list = account.transaction_set.all()
        context['transactions'] = transactions
    except Cuenta.DoesNotExist:
        pass

    context["styles"] = fill_navbar_style(customer=user.cliente)

    return render(request, 'cuentas/details.html', context)


@login_required()
def transfer_page(request):
    """
    View function for Transfer Page of site.
    """
    if request.method == 'POST':
        return handle_transfer_post(request)

    user: User = request.user
    context: dict = {"styles": fill_navbar_style(customer=user.cliente)}
    accounts = user.cuenta_set.exclude(type=Cuenta.AccountType.SAVINGS_USD)
    all_accounts = user.cuenta_set.all()
    context["accounts"] = accounts
    context["all_accounts"] = all_accounts
    return render(request, 'cuentas/transfers.html', context)


def handle_transfer_post(request):
    to_id = request.POST.get('to')
    from_id = request.POST.get('from')
    amount = request.POST.get('amount')

    if to_id is None or from_id is None:
        messages.error(request, 'No account to transfer to or from')
        return redirect('transfers')

    if to_id == from_id:
        messages.error(request, 'Can not transfer to the same Account')
        return redirect('transfers')

    from_id = int(from_id)

    try:
        to_id = int(to_id)
    except ValueError:
        using_alias = True

    if amount is None:
        messages.error(request, 'No amount specified')
        return redirect('transfers')

    amount = float(amount)
    if amount <= 0:
        messages.error(request, 'Amount must be greater than 0')
        return redirect('transfers')

    try:
        from_account = Cuenta.objects.get(pk=from_id)

        if from_account.balance < amount:
            messages.error(request,
                           f'Not enough balance in account,'
                           f' please try again with an amount smaller than {from_account.balance_currency()}')
            return redirect('transfers')

        if not using_alias:
            to_account = Cuenta.objects.get(pk=to_id)
        elif to_id != from_account.alias:
            to_account = Cuenta.objects.get(Q(alias=to_id) | Q(iban=to_id))
        else:
            messages.error(request, 'Can not transfer to the same Account')
            return redirect('transfers')

        if (
                to_account.type == Cuenta.AccountType.SAVINGS_USD.value and
                from_account.type != Cuenta.AccountType.SAVINGS_USD.value) or (
                from_account.type == Cuenta.AccountType.SAVINGS_USD.value and
                to_account.type != Cuenta.AccountType.SAVINGS_USD.value):
            messages.error(request,
                           'Only from a USD Savings Account is allowed to transfer to another USD Savings accounts')
            return redirect('transfers')

        from_account.balance -= amount
        to_account.balance += amount

        transfer_sent = Transaction(amount=(-amount), account=from_account,
                                    operation=Transaction.OperationType.TRANSFER.value,
                                    description=f"To {to_account.customer.last_name}, "
                                                f"{to_account.customer.first_name} "
                                                f"({to_account.iban})")

        transfer_received = Transaction(amount=amount, account=to_account,
                                        operation=Transaction.OperationType.TRANSFER.value,
                                        description=f"From {from_account.customer.last_name}, "
                                                    f"{from_account.customer.first_name} "
                                                    f"({from_account.iban})")

        from_account.save()
        transfer_sent.save()

        to_account.save()
        transfer_received.save()

        messages.success(request, 'Transfer successful')
    except Cuenta.DoesNotExist:
        messages.error(request, 'Account not found')
        return redirect('transfers')

    return redirect('me')
