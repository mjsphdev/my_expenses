# Generated by Django 3.2.5 on 2021-08-05 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billspayments',
            name='month',
            field=models.CharField(default='8,2021', max_length=50, unique=True),
        ),
    ]
