# Generated by Django 5.1 on 2024-09-16 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0024_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeleave',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='guest.status'),
            preserve_default=False,
        ),
    ]
