# Generated by Django 5.1 on 2024-09-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0013_leavepolicymonthly_leave_alter_leavepolicymonthly_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavepolicymonthly',
            name='leave',
        ),
        migrations.AlterField(
            model_name='leavepolicymonthly',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
