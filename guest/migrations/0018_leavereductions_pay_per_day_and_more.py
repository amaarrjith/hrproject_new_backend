# Generated by Django 5.1 on 2024-09-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0017_leavereductions'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereductions',
            name='pay_per_day',
            field=models.BigIntegerField(default=0, verbose_name=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leavereductions',
            name='reduction_amount',
            field=models.BigIntegerField(default=0, verbose_name=''),
            preserve_default=False,
        ),
    ]
