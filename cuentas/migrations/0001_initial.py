# Generated by Django 4.1 on 2022-08-22 02:54

import cuentas.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.CharField(default=cuentas.models.account_id_generator, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('CA', 'Current Account'), ('SA', 'Savings Account'), ('SAU', 'Savings Account (USD)')], default='CA', max_length=3)),
                ('iban', models.CharField(default='-', max_length=200, null=True)),
                ('balance', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'CUENTAS',
            },
        ),
    ]