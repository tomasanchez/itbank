from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from branches.models import Address, Branch
from cliente.models import Cliente
from cuentas.models import Cuenta
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'number', 'city', 'state', 'country', 'zip_code']


class BranchSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Branch
        fields = ['name', 'address']


class TarjetaSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Tarjeta
        fields = ['brand', 'type', 'number', 'cvv', 'valid_from', 'expiration_end']


class CuentaSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Cuenta
        fields = ['iban', 'type', 'alias', 'balance']


class PrestamoCreateSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username', write_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d", required=False, default=datetime.now)

    class Meta:
        model = Prestamo
        fields = ['type', 'date', 'total', "customer", "date"]

    def validate(self, data):
        amount = data['total']

        try:
            amount = float(amount)
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")
        except ValueError:
            raise serializers.ValidationError("Amount must be a number")

        loan_type = data['type']
        if loan_type not in Prestamo.LoanType.values:
            raise serializers.ValidationError("Invalid loan type")

        username = data['customer']["username"]
        if username is None:
            raise serializers.ValidationError("Username is required")

        try:
            customer = User.objects.get(username=username).cliente
        except User.DoesNotExist:
            raise serializers.ValidationError("Customer does not exists")

        max_loan = Prestamo.get_max_loan(customer)

        if amount > max_loan:
            raise serializers.ValidationError("Amount is greater than the maximum allowed loan")

        return data

    def create(self, validated_data):
        customer = User.objects.get(username=validated_data['customer']["username"]).cliente
        loan = Prestamo(
            customer=customer,
            type=validated_data['type'],
            total=validated_data['total'],
            date=validated_data['date']
        )
        loan.save()
        return loan


class PrestamoSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Prestamo
        fields = ['type', 'date', 'total']


class ClienteSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    address = AddressSerializer(read_only=True)

    class Meta:
        fields = ('type', 'dni', 'address',)
        model = Cliente


class UserSerializer(serializers.ModelSerializer):
    customer = ClienteSerializer(many=False, read_only=True, source='cliente')
    accounts = CuentaSerializer(many=True, read_only=True, source='cuenta_set')
    cards = TarjetaSerializer(many=True, read_only=True, source='tarjeta_set')
    loans = PrestamoSerializer(many=True, read_only=True, source='cliente.prestamo_set')
    extra_kwargs = {'password': {'write_only': True}}

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'customer', 'accounts', "cards", 'loans')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
