# Generated by Django 3.2.5 on 2021-08-08 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_budget_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='month',
            field=models.CharField(default='8-2021', max_length=10, unique=True),
        ),
    ]