# Generated by Django 4.2.3 on 2023-07-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.IntegerField(unique=True, verbose_name='یوزرنیم'),
        ),
    ]
