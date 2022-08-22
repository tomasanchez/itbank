# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cuenta(models.Model):
    id = models.IntegerField(primary_key=True)
    cliente_id = models.IntegerField()
    balance = models.IntegerField()
    iban = models.CharField(max_length=200)
    tipo_cuenta_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'CUENTAS'


class Empleado(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    hire_date = models.DateTimeField(auto_now=True)
    dni = models.IntegerField()
    branch_id = models.IntegerField()
    direccion_id = models.ForeignKey()

    class Meta:
        managed = False
        db_table = 'EMPLEADOS'


class Movimientos(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    account_id = models.IntegerField()
    operation_tipe = models.CharField(max_length=200)
    amount = models.IntegerField(auto_now=True)
    changet_at = models.CharField()

    class Meta:
        managed = False
        db_table = 'MOVIMIENTOS'


class Prestamo(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    total = models.IntegerField()
    customer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'PRESTAMO'


class Tarjeta(models.Model):
    numero = models.IntegerField(primary_key=True)
    cvv = models.CharField(max_length=200)
    fecha_otorgamiento = models.CharField(max_length=200)
    fecha_expiracion = models.CharField(max_length=200)
    tipo_id = models.CharField(max_length=200)
    customer_id = models.IntegerField()
    tipo_tarjeta_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TARJETAS'
