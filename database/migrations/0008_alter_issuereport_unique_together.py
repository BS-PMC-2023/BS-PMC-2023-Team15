# Generated by Django 4.2 on 2023-04-06 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_alter_issuereport_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='issuereport',
            unique_together={('item_serial_number', 'student_email', 'date_opened')},
        ),
    ]
