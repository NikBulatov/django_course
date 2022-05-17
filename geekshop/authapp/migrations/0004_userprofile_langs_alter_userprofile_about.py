# Generated by Django 4.0.4 on 2022-05-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, default='RU', max_length=5, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
    ]