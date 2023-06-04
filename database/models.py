from django.db import models
from django.conf import settings


# Create your models here.

# model named students - full name, id, email, phone number, password
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


# model named equipement: serial number - string, category, brand, model, details
class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='equipment/', default='default.png')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.serial_number + " " + self.brand + " " + self.model

    class Meta:
        verbose_name_plural = "Equipment"


# model named reservations: email-PK, ID number-PK, item - ID, date - from, date - to
class Reservation(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    item = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='item')
    date_from = models.DateField()
    date_to = models.DateField()
    id = models.AutoField(primary_key=True)
    returned = models.BooleanField(default=False)
    statuses = [('B', 'Borrowed'), ('Q', 'In queue'), ('M', 'malfunction'), ('A', 'Available'),
                ('W', 'Waiting'), ('P', 'Passed')]
    status = models.CharField(max_length=100, choices=statuses, default=statuses[3])

    class Meta:
        unique_together = ('student', 'item', 'date_from', 'status')

    def __str__(self):
        return self.student.email


# model named issue report: item_serial_number,student_email, date when opened, date when closed,status details (no foreign keys)
class IssueReport(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    item = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    date_opened = models.DateField()
    date_closed = models.DateField(default=None, null=True, blank=True)
    status = models.ForeignKey('IssueStatus', on_delete=models.CASCADE)
    details = models.TextField(max_length=1000, default='No details', blank=False, null=False, primary_key=True)

    class Meta:
        unique_together = (('student', 'item', 'date_opened', 'date_closed', 'status'),)

    def __str__(self):
        return f'{self.item}: {self.details}'


# Studio: room - pk, name, image - default: default.png, details
class Studio(models.Model):
    room = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='studios/', default='default.png')

    def __str__(self):
        return f"{self.room} - {self.name}"


# IssueStatus - GOOD, BAD, SEVERE
class IssueStatus(models.Model):
    status = models.CharField(max_length=100, primary_key=True)

    class Meta:
        verbose_name_plural = "Issue Status"

    def __str__(self):
        return self.status
