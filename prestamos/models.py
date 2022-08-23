from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cliente.models import Cliente
from cuentas.models import Transaction, Cuenta


# Create your models here.


class Prestamo(models.Model):
    class LoanType(models.TextChoices):
        MORTGAGE = 'MO', 'Mortgage'
        PERSONAL = 'PE', 'Personal'
        PLEDGE = 'PL', 'Pledge'
        STUDENT = 'ST', 'Student'
        VEHICLE = 'VE', 'Vehicle'

    customer = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=2,
        choices=LoanType.choices)
    date = models.DateField(default=datetime.now)
    total = models.FloatField()
    cancelled = models.FloatField(default=0.0)

    class Meta:
        db_table = 'PRESTAMOS'

    def __str__(self):
        return f"{self.customer.user.username}: ${self.total} | {self.date} ({self.get_type_display()})"

    @staticmethod
    def get_max_loan(costumer: Cliente) -> float:
        """
        Returns the maximum loan amount for a given costumer
        """
        match costumer.type:
            case costumer.CustomerType.CLASSIC:
                return 100_000.00
            case costumer.CustomerType.GOLD:
                return 300_000.00
            case costumer.CustomerType.BLACK:
                return 500_000.00
            case _:
                return 0.00


@receiver(post_save, sender=Prestamo)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        # Update account balance
        savings_account = instance.customer.user.cuenta_set.get(type=Cuenta.AccountType.SAVINGS.value)
        if savings_account is not None:
            savings_account.balance += instance.total
            savings_account.save()
            transaction = Transaction(
                account=savings_account,
                operation=Transaction.OperationType.DEPOSIT.value,
                amount=instance.total,
                description=f"{instance.get_type_display()} Loan"
            )
            transaction.save()
