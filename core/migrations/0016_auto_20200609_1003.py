# Generated by Django 2.2.10 on 2020-06-09 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_slider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='subtitle',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
