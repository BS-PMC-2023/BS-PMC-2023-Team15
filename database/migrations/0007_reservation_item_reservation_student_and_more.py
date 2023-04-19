# Generated by Django 4.2 on 2023-04-14 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_alter_reservation_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='database.equipment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='database.student'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('student', 'item', 'date_from')},
        ),
    ]