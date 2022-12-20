# Generated by Django 4.1.1 on 2022-11-29 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0005_alter_book_isbn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 29, 17, 30, 35, 788114)),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='issue_date',
            field=models.DateField(default=datetime.datetime(2022, 11, 29, 17, 30, 35, 788099)),
        ),
    ]
