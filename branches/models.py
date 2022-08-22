import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'DIRECCIONES'

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}"


class Branch(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, default=None, )

    class Meta:
        db_table = 'SUCURSALES'

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    dni = models.PositiveIntegerField(unique=True)
    hire_date = models.DateField(default=datetime.date.today)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        db_table = 'EMPLEADOS'

    def __str__(self):
        return f"{self.user}"
