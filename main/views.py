from django.contrib.auth.models import User
from django.dispatch import receiver
from django.views.decorators.cache import never_cache
from django.contrib import messages

from accounts import forms
from database.models import Category, Equipment, IssueReport
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.shortcuts import get_object_or_404
from database.models import Reservation, Student
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
import base64, qrcode, io
from django.views.decorators.http import require_http_methods
from django.db.models.signals import post_save, post_delete

@login_required
def main_view(request):
    return render(request, 'categories.html',{} )

@login_required
def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'products.html', {'categories': categories})

@login_required
def studio_view(request):
    categories = Category.objects.all()
    return render(request, 'studio.html', {'categories': categories})

@login_required
def podcast_view(request):
    categories = Category.objects.all()
    return render(request, 'podcast.html', {'categories': categories})
@login_required
def malfunction_view(request, serial):
    return render(request, 'malfunction.html', {"item": serial})

def malfunction_send(request):
    # add malfunction to DB
    return redirect('main')
@login_required
def policy_view(request):
    return render(request, 'policy.html',)

@login_required
def category_view(request, category):
    # category = Category.objects.get(name=category)
    items = Equipment.objects.filter(category=category)
    return render(request, 'catalog.html', {"items": items})

@login_required
@never_cache
def item_detail_view(request, item):
    # Get the category object based on the category name
    # item = get_object_or_404(Category, serial_number=item)
    form = ReservationForm()
    s = 'A'
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        u =request.user
        if u.username =='admin':
            u = u.email
        student = Student.objects.get(email=u)
        item_serial_number = item
        date_from = form.data['date_from']
        date_to = form.data['date_to']

        # catch ValidationError
        item_to_borrow = Equipment.objects.get(serial_number=item_serial_number)
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            if date_from > date_to:
                raise ArithmeticError
            reservation = Reservation(student=student, item=item_to_borrow, date_from=date_from, date_to=date_to, status='B')
            reservation.save()
            s = 'Q'
            messages.success(request, 'Item reserved successfully')

        except ValueError:
            messages.error(request, 'Invalid date format')
            # return HttpResponse("Invalid date format")
        except ArithmeticError:
            messages.error(request, 'Invalid date range')
        except:
            messages.error(request, 'Could not reserve item: already reserved')
            s = 'Q'

            # return HttpResponse("Invalid date range")

    try:
        item_to_borrow = Equipment.objects.get(serial_number=item)
        if Reservation.status == 'B' or Reservation.status == 'Q':
            Reservation.objects.get(item=item_to_borrow, date_to__gte=datetime.today())
            s = 'Q'
    except:
        s = 'A'

    result = Equipment.objects.get(serial_number=item)
    issues = IssueReport.objects.filter(item=result)
    date_min = datetime.now().date().isoformat()

    # qr code
    img = qrcode.make(item)
    byteIO = io.BytesIO()
    img.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()
    image_data = base64.b64encode(byteArr).decode('utf-8')
    return render(request, 'details.html', {"form": form, "item": result, "issues": issues, "date_min": date_min, "qr": image_data, "status": s})

def requests(request):
    return render(request, 'requests.html', )

def overdue(request):
    today = date.today()
    reservations = Reservation.objects.filter(returned=False, date_to__lt=today)
    context = {'reservations': reservations}
    return render(request, 'overdue.html', context)




def profile_view(request):
    usr = request.user
    if request.user.username == "admin": usr = request.user.email
    student = Student.objects.get(email=usr)
    my_items = Reservation.objects.filter(student=student.id, returned=False)

    if request.user.username == "lecturer": usr = request.user.email
    student = Student.objects.get(email=usr)
    my_items = Reservation.objects.filter(student=student.id, returned=False)

    return render(request, 'profile.html', {"my_items": my_items})

def profile_return(request,item):
    if request.method != "POST":
        return redirect('main')
    student = Student.objects.get(email=request.user.email)
    reservation = Reservation.objects.get(id=item, student=student.id)
    reservation.returned = True
    reservation.save()
    return redirect('profile')

def mal_view(request):
    return render(request, 'mal.html', )

def history(request,user):
    if user == None: user = request.user
    users = User.objects.all()

    if user == "admin": user = "admin@gmail.com"
    student = Student.objects.get(email=user)
    my_items = Reservation.objects.filter(student=student.id)

    if user == "lecturer": user = "lecturer@gmail.com"
    student = Student.objects.get(email=user)
    my_items = Reservation.objects.filter(student=student.id)

    return  render(request, 'history.html', {"reservations": my_items, "users": users})

@receiver(post_save, sender=Student)
def new_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create(username=instance.email)
        user.set_password(instance.password)
        user.save()


@receiver(post_delete, sender=Student)
def del_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.email)
        user.delete()
    except:
        pass



@login_required
def search(request):
    q = request.GET.get('query')
    if q is None:
        return redirect('/')
    by_serial = Equipment.objects.filter(serial_number__contains=q)
    by_category = Equipment.objects.filter(category__name__contains=q)
    by_brand = Equipment.objects.filter(brand__contains=q)
    by_model = Equipment.objects.filter(model__contains=q)
    s = by_serial.union(by_category, by_brand, by_model)
    if s.exists():
        return render(request,'catalog.html', {'items': s})

    return render(request,'catalog.html', {'items': None})


def stats(request):

    categories = Category.objects.all()
    items = Equipment.objects.all()

    # number of item reservation per item per category in this form "category": {"item": number_of_reservations}
    reservations = {}
    for category in categories:
        reservations[category.name] = {}
        for item in items.filter(category=category):
            reservations[category.name][f"{item.brand} {item.model}"] = Reservation.objects.filter(item=item, item__category=category).count()

    return render(request, 'statistics.html', {"reservations": reservations})

import csv
from django.shortcuts import render
from database.models import Student

from django.core.exceptions import ObjectDoesNotExist

def addstudents(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return render(request, 'addstudents.html', {'error': 'Please select a CSV file.'})
        if not csv_file.name.endswith('.csv'):
            return render(request, 'addstudents.html', {'error': 'Please upload a valid CSV file.'})

        csv_text = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_text)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            full_name = row[0]
            id_str = row[1]
            email = row[2]
            phone_number_str = row[3]
            password = row[4]

            # Validate the id field
            try:
                id = int(id_str)
            except ValueError:
                return render(request, 'addstudents.html', {'error': f"Invalid value for 'id' field: {id_str}."})

            # Validate the phone_number field
            try:
                phone_number = int(phone_number_str)
            except ValueError:
                return render(request, 'addstudents.html', {'error': f"Invalid value for 'phone_number' field: {phone_number_str}."})

            try:
                # Check if student already exists
                student = Student.objects.get(id=id)
                continue  # Skip adding the student and proceed to the next row
            except ObjectDoesNotExist:
                pass

            student = Student(
                full_name=full_name,
                id=id,
                email=email,
                phone_number=phone_number,
                password=password
            )
            student.save()

        return render(request, 'addstudents.html', {'success': 'CSV file uploaded successfully.'})

    return render(request, 'addstudents.html')


# def pass_item_view(request, item):
#     student = Student.objects.all()
#     #reservation = Reservation.objects.get(id=item)
#  #   if request.method == "POST":
#         #if user == "admin": user = "admin@gmail.com"
#         #student = Student.objects.get(email=user)
#
#     return render(request, 'pass_item.html', {"item": item, "student": student})
#
#
# def pass_item_to_student(request, item, student):
#     if request.method != "POST":
#         return redirect('main')
#     student = Student.objects.get(id=student)
#     reservation = Reservation.objects.get(id=item)
#     reservation.student = student
#     reservation.save()
#     return redirect('profile')


def pass_item_view(request, item):
    students = Student.objects.all()
    return render(request, 'pass_item.html', {"item": item, "students": students})

def pass_item_to_student(request, item, student):
    date = datetime.today()

    if request.method == "POST":
        item = Equipment.objects.get(serial_number=item)
        student = Student.objects.get(full_name=student)
        reservation = Reservation.objects.create(student=student, item=item, date_from=date,
                                                date_to=date, returned=False, status='B')
        reservation.save()
        return redirect('profile')
    else:
        return redirect('/')


# def pass_item_to_student_confirm(request, item,student):
#     if request.method == "POST":
#         reservation=Reservation.objects.create(student=student,item=item,date_from=datetime.date.today(),
#                                            date_to=datetime.date.today(),returned=False,status='B')
#         reservation.save()
#         return redirect('profile')
#     else:
#         return redirect('/')

