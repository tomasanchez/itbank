# Generated by Django 4.1 on 2022-08-22 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tarjetas.card_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('D', 'Debit'), ('C', 'Credit'), ('G', 'Gift')], default='D', max_length=1)),
                ('brand', models.CharField(choices=[('VISA', 'Visa'), ('MASTERCARD', 'Mastercard'), ('AMEX', 'American Express')], default='VISA', max_length=25)),
                ('number', models.CharField(default=tarjetas.card_utils.generate_card_number, max_length=16)),
                ('cvv', models.CharField(default=tarjetas.card_utils.generate_cvv, max_length=4)),
                ('valid_from', models.DateField(auto_now=True)),
                ('expiration_end', models.DateField(default=tarjetas.card_utils.expiration_date_generator, editable=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'TARJETAS',
                'unique_together': {('number', 'cvv')},
            },
        ),
    ]
