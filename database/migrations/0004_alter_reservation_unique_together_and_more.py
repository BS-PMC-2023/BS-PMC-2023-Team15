# Generated by Django 4.2 on 2023-06-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_reservation_returned_alter_reservation_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('B', 'Borrowed'), ('Q', 'In queue'), ('M', 'malfunction'), ('A', 'Available'), ('W', 'Waiting'), ('P', 'Passed')], default=('A', 'Available'), max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('student', 'item', 'date_from', 'status')},
        ),
    ]