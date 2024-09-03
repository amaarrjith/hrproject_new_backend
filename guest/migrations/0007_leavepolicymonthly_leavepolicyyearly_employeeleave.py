# Generated by Django 5.1 on 2024-09-03 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0006_status_bonus_status_reduction_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeavePolicyMonthly',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('casual_leaves', models.IntegerField()),
                ('sick_leaves', models.IntegerField()),
                ('half_day_leaves', models.IntegerField()),
                ('month', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LeavePolicyYearly',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('casual_leaves', models.IntegerField()),
                ('sick_leaves', models.IntegerField()),
                ('half_day_leaves', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('casual_leaves', models.IntegerField()),
                ('sick_leaves', models.IntegerField()),
                ('half_day_leaves', models.IntegerField()),
                ('excess_leave', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.employees')),
            ],
        ),
    ]
