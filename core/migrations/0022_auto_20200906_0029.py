# Generated by Django 2.2.10 on 2020-09-05 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_item_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='mobile_number',
            field=models.CharField(max_length=200),
        ),
    ]
