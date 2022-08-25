from django.contrib.auth.models import User
from rest_framework import serializers

from branches.models import Address
from cliente.models import Cliente
from cuentas.models import Cuenta
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'number', 'city', 'state', 'country', 'zip_code']


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


class PrestamoSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Prestamo
        fields = ['type', 'date', 'total', ]


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
