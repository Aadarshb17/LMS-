# Generated by Django 4.1.1 on 2022-12-12 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0010_alter_issuedbook_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 1, 11, 17, 18, 16, 465520)),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='issue_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 12, 17, 18, 16, 465505)),
        ),
    ]
