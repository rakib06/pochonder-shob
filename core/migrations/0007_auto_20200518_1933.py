# Generated by Django 2.2.10 on 2020-05-18 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200518_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Offer',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Offer'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.ManyToManyField(default='', to='core.Size'),
        ),
    ]
