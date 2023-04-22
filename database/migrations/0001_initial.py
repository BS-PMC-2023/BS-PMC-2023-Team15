# Generated by Django 4.2 on 2023-04-12 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('serial_number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('details', models.TextField(max_length=1000)),
                ('image', models.ImageField(default='default.png', upload_to='equipment/')),
            ],
            options={
                'verbose_name_plural': 'Equipment',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('full_name', models.CharField(max_length=100)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('room', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField(max_length=1000)),
                ('image', models.ImageField(default='default.png', upload_to='studios/')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('student_email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('student_id', models.CharField(max_length=100)),
                ('item_serial_number', models.CharField(max_length=100)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
            ],
            options={
                'unique_together': {('student_email', 'student_id', 'item_serial_number')},
            },
        ),
        migrations.CreateModel(
            name='IssueReport',
            fields=[
                ('item_serial_number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('student_email', models.CharField(max_length=100)),
                ('date_opened', models.DateField()),
                ('date_closed', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('details', models.TextField(max_length=1000)),
            ],
            options={
                'unique_together': {('item_serial_number', 'student_email', 'date_opened')},
            },
        ),
    ]
