# Generated by Django 4.2 on 2023-04-14 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_issuestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuereport',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.issuestatus'),
        ),
    ]