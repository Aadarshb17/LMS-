# Generated by Django 4.1.1 on 2022-12-14 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0015_alter_issuedbook_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 1, 13, 19, 46, 46, 612165)),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='issue_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 14, 19, 46, 46, 612151)),
        ),
    ]
