# Generated by Django 5.1 on 2024-09-03 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0002_login_employee_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='employee_id',
            new_name='employee',
        ),
    ]
