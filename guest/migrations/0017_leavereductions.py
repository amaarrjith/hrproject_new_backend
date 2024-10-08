# Generated by Django 5.1 on 2024-09-06 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0016_rename_excess_leave_employeeleave_excess_leave_monthcl_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='leaveReductions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excess_leave_monthcl', models.IntegerField()),
                ('excess_leave_monthsl', models.IntegerField()),
                ('excess_leave_monthhalf', models.IntegerField()),
                ('excess_leave_yrcl', models.IntegerField()),
                ('excess_leave_yrsl', models.IntegerField()),
                ('excess_leave_yrhalf', models.IntegerField()),
                ('for_year', models.IntegerField()),
                ('total_excess_leave', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.employees')),
                ('for_month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.month')),
            ],
        ),
    ]
