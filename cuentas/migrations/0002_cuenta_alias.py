# Generated by Django 4.1 on 2022-08-22 15:17

import cuentas.accounts_util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='alias',
            field=models.CharField(default=cuentas.accounts_util.generate_alias, max_length=200),
        ),
    ]
