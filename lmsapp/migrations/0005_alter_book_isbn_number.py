# Generated by Django 4.1.1 on 2022-11-24 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0004_remove_student_email_remove_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.IntegerField(default=1, max_length=15),
        ),
    ]
