from django.db import models
from django.conf import settings
# Create your models here.

#model named students - full name, id, email, phone number, password
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=100)
    phone_number = models.IntegerField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='categories/', default='default.png')
    description = models.TextField(max_length=1000, default='No description')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


#model named equipement: serial number - string, category, brand, model, details
class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='equipment/', default='default.png')

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name_plural = "Equipment"


#model named reservations: email-PK, ID number-PK, item - ID, date - from, date - to
class Reservation(models.Model):
    student_email = models.CharField(max_length=100,  primary_key=True)
    student_id = models.CharField(max_length=100)
    item_serial_number = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()

    class Meta:
        unique_together = ('student_email', 'student_id', 'item_serial_number')

    def __str__(self):
        return self.student_email


#model named issue report: item_serial_number,student_email, date when opened, date when closed,status details (no foreign keys)
class IssueReport(models.Model):
    item_serial_number = models.CharField(max_length=100, primary_key=True)
    student_email = models.CharField(max_length=100)
    date_opened = models.DateField()
    date_closed = models.DateField()
    status = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)

    class Meta:
        unique_together = ('item_serial_number', 'student_email', 'date_opened')

    def __str__(self):
        return f"{self.item_serial_number} - {self.student_email} - {self.date_opened}"

# Studio: room - pk, name, image - default: default.png, details
class Studio(models.Model):
    room = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='studios/', default='default.png')

    def __str__(self):
        return f"{self.room} - {self.name}"


# Category - name
