import datetime
import locale
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from schwifty import IBAN

from cliente.models import Cliente
from .accounts_util import generate_alias


def account_id_generator() -> str:
    """
        Create a random id for a new account.
    """
    return str(uuid.uuid4().int)[:10]


# Create your models here.

class Cuenta(models.Model):
    class AccountType(models.TextChoices):
        CURRENT = 'CA', 'Current Account'
        SAVINGS = 'SA', 'Savings Account'
        SAVINGS_USD = 'SAU', 'Savings Account (USD)'

    id = models.CharField(primary_key=True,
                          default=account_id_generator,
                          max_length=10,
                          editable=False,
                          null=False, )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=3,
        choices=AccountType.choices,
        default=AccountType.CURRENT,
    )
    iban = models.CharField(max_length=200,
                            null=True,
                            default="-",
                            )
    balance = models.FloatField(default=0.0)
    alias = models.CharField(max_length=200, default=generate_alias)

    class Meta:
        db_table = 'CUENTAS'

    def __str__(self):
        return f"{self.iban} - {self.customer.username}'s {self.get_type_display()}"

    def balance_currency(self) -> str:
        """
            Return the balance of the account in a string format.
        """
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        if self.type == Cuenta.AccountType.SAVINGS_USD.value:
            return f"US{locale.currency(self.balance, grouping=True)}"
        else:
            return locale.currency(self.balance, grouping=True)


class Transaction(models.Model):
    class OperationType(models.TextChoices):
        DEPOSIT = 'DE', 'Deposit'
        WITHDRAW = 'WI', 'Withdraw'
        TRANSFER = 'TR', 'Transfer'

    account = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    operation = models.CharField(choices=OperationType.choices, max_length=2)
    amount = models.FloatField()
    date = models.DateTimeField(default=datetime.date.today, editable=False)

    class Meta:
        db_table = 'MOVIMIENTOS'

    def __str__(self):
        return f"{self.balance_currency()}\t" \
               f"({self.get_operation_display()} {datetime.date.strftime(self.date, '%m/%d/%y')})"

    def balance_currency(self) -> str:
        """
            Return the balance of the account in a string format.
        """
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        if self.account.type == Cuenta.AccountType.SAVINGS_USD.value:
            return f"US{locale.currency(self.amount, grouping=True)}"
        else:
            return locale.currency(self.amount, grouping=True)


@receiver(post_save, sender=Cuenta)
def populate_iban(sender, instance, created, **kwargs):
    if created:
        data = Cuenta.objects.get(id=instance.id)
        data.iban = str(IBAN.generate('DE', bank_code='10001138', account_code=str(data.id)))
        data.save()


@receiver(post_save, sender=Cliente)
def create_account_for_costumer(sender, instance, created, **kwargs):
    if created:
        customer = instance.user
        account = Cuenta(customer=customer, type=Cuenta.AccountType.SAVINGS.value)
        account.save()
        match instance.type:
            case instance.CustomerType.GOLD:
                account_1 = Cuenta(customer=customer,
                                   type=Cuenta.AccountType.SAVINGS_USD.value)
                account_1.save()
            case instance.CustomerType.BLACK:
                account_2 = Cuenta(customer=customer,
                                   type=Cuenta.AccountType.SAVINGS_USD.value)
                account_2.save()
                account_3 = Cuenta(
                    customer=customer,
                    type=Cuenta.AccountType.CURRENT.value)
                account_3.save()
