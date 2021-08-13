# Generated by Django 3.2.5 on 2021-08-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_particulier_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codeinstance',
            name='associatedPhone',
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='associatedUser',
            field=models.CharField(default='username', max_length=20),
        ),
    ]
