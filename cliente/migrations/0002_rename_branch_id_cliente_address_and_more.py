# Generated by Django 4.1 on 2022-08-21 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='branch_id',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='direccion_id',
        ),
        migrations.AddField(
            model_name='cliente',
            name='branch',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='branches.branch'),
        ),
    ]
