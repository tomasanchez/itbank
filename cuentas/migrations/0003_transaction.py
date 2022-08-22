# Generated by Django 4.1 on 2022-08-22 18:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_cuenta_alias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('DE', 'Deposit'), ('WI', 'Withdraw'), ('TR', 'Transfer')], max_length=2)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(default=datetime.date.today, editable=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuentas.cuenta')),
            ],
            options={
                'db_table': 'MOVIMIENTOS',
            },
        ),
    ]