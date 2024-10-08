# Generated by Django 5.1 on 2024-09-03 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0005_bonus_added_on_reduction_added_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=50, verbose_name='')),
            ],
        ),
        migrations.AddField(
            model_name='bonus',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='guest.status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reduction',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='guest.status'),
            preserve_default=False,
        ),
    ]
