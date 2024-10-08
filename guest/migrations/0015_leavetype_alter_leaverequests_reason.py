# Generated by Django 5.1 on 2024-09-05 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0014_remove_leavepolicymonthly_leave_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='leavetype',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='leaverequests',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.leavetype'),
        ),
    ]
