# Generated by Django 4.2 on 2023-04-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_alter_issuereport_date_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]