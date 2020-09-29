# Generated by Django 3.1.1 on 2020-09-09 10:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^0?[1:9]{1}\\d{9}$')]),
        ),
    ]
