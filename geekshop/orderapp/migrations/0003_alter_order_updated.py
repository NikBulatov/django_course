# Generated by Django 4.0.5 on 2022-06-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_remove_order_paided_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлён'),
        ),
    ]