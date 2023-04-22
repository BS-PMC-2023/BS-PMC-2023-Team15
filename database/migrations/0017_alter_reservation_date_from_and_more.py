# Generated by Django 4.2 on 2023-04-15 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_equipment_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='database.student'),
        ),
    ]
