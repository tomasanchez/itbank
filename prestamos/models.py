from datetime import datetime

from django.db import models

from cliente.models import Cliente


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
