# Generated by Django 3.2.5 on 2021-08-06 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_particulier_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='particulier',
            name='phone_number',
            field=models.IntegerField(default='2250000000000', unique=True),
        ),
    ]