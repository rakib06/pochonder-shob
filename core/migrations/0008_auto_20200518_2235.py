# Generated by Django 2.2.10 on 2020-05-18 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200518_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.AddField(
            model_name='size',
            name='for_item',
            field=models.ManyToManyField(to='core.Item'),
        ),
    ]
