# Generated by Django 2.2.10 on 2020-05-22 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200522_0552'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity_available',
            field=models.IntegerField(default=1, verbose_name='Available Quantity'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='Confirm Order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='ordered quantity'),
        ),
    ]
