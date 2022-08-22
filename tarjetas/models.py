import datetime

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from cliente.models import Cliente
from tarjetas.card_utils import expiration_date_generator, generate_card_number, generate_cvv


class Tarjeta(models.Model):
    class CardType(models.TextChoices):
        DEBIT = 'D', 'Debit'
        CREDIT = 'C', 'Credit'
        GIFT = 'G', 'Gift'

    class CardBrand(models.TextChoices):
        VISA = 'VISA', "Visa"
        MASTERCARD = 'MASTERCARD', "Mastercard"
        AMEX = 'AMEX', "American Express"

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=1,
        choices=CardType.choices,
        default=CardType.DEBIT
    )
    brand = models.CharField(
        max_length=25,
        choices=CardBrand.choices,
        default=CardBrand.VISA
    )
    number = models.CharField(max_length=16, default=generate_card_number)
    cvv = models.CharField(max_length=4, default=generate_cvv)
    valid_from = models.DateField(auto_now=True, editable=False)
    expiration_end = models.DateField(default=expiration_date_generator, editable=False)

    class Meta:
        unique_together = ('number', 'cvv')
        db_table = 'TARJETAS'

    def __str__(self):
        if self.brand == self.CardBrand.AMEX.value:
            return f"XXX-XXXXXX-{self.number[10:]}"
        else:
            return f"XXXX-XXXX-XXXX-{self.number[12:]}"

    def display_number(self):
        if self.brand == self.CardBrand.AMEX.value:
            return f"{self.number[:3]} {self.number[3:9]} {self.number[10:]}"
        else:
            return f"{self.number[:4]} {self.number[4:8]} {self.number[8:12]} {self.number[12:]}"

    def logo(self):
        ext = "svg"
        return self.brand.lower() + f".{ext}"

    def display_expiration(self):
        return datetime.date.strftime(self.expiration_end, '%m/%y')


@receiver(post_save, sender=Cliente)
def create_cards_for_costumer(sender, instance, created, **kwargs):
    if created:
        customer = instance.user
        debit_card = Tarjeta(customer=customer)
        debit_card.save()
        match instance.type:
            case instance.CustomerType.GOLD:
                number = generate_card_number(card_brand="MASTERCARD")
                mastercard = Tarjeta(customer=customer, type=Tarjeta.CardType.CREDIT,
                                     brand=Tarjeta.CardBrand.MASTERCARD, number=number)
                mastercard.save()
            case instance.CustomerType.BLACK:
                visa = Tarjeta(customer=customer, type=Tarjeta.CardType.CREDIT, brand=Tarjeta.CardBrand.VISA)
                visa.save()
                cvv = generate_cvv(4)
                number = generate_card_number(card_brand="AMEX")
                amex = Tarjeta(customer=customer, type=Tarjeta.CardType.CREDIT, brand=Tarjeta.CardBrand.AMEX,
                               cvv=cvv, number=number)
                amex.save()
