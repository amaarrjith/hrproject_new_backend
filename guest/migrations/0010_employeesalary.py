# Generated by Django 5.1 on 2024-09-04 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0009_rename_casual_leaves_employeeleave_casual_leaves_monthly_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='employeeSalary',
            fields=[
                ('salary_id', models.AutoField(primary_key=True, serialize=False)),
                ('base_package', models.BigIntegerField()),
                ('total_reduction', models.BigIntegerField()),
                ('total_bonus', models.BigIntegerField()),
                ('leave_reductions', models.BigIntegerField()),
                ('generated_salary', models.BigIntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.employees')),
                ('salary_month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.month')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.status')),
            ],
        ),
    ]
