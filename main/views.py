from django.contrib.auth.models import User
from django.dispatch import receiver
from django.views.decorators.cache import never_cache
from django.contrib import messages
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
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        student = Student.objects.get(email=request.user)
        item_serial_number = item
        date_from = form.data['date_from']
        date_to = form.data['date_to']

        # catch ValidationError
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            if date_from > date_to: raise ArithmeticError
            item_to_borrow = Equipment.objects.get(serial_number=item_serial_number)
            reservation = Reservation(student=student, item=item_to_borrow, date_from=date_from, date_to=date_to)
            reservation.save()
            messages.success(request, 'Item reserved successfully')

        except ValueError:
            messages.error(request, 'Invalid date format')
            # return HttpResponse("Invalid date format")
        except ArithmeticError:
            messages.error(request, 'Invalid date range')
        except:
            messages.error(request, 'Could not reserve item: already reserved')

            # return HttpResponse("Invalid date range")



    result = Equipment.objects.get(serial_number=item)
    issues = IssueReport.objects.filter(item=result)
    date_min = datetime.now().date().isoformat()

    # qr code
    img = qrcode.make(item)
    byteIO = io.BytesIO()
    img.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()

    image_data = base64.b64encode(byteArr).decode('utf-8')



    return render(request, 'details.html', {"form": form, "item": result, "issues": issues, "date_min": date_min, "qr": image_data})


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
    return render(request, 'profile.html', {"my_items": my_items})

def profile_return(request,item):
    if request.method != "POST":
        return redirect('main')
    student = Student.objects.get(email=request.user.email)
    reservation = Reservation.objects.get(id=item, student=student.id)
    reservation.returned = True
    reservation.save()
    return redirect('profile')



def history(request,user):
    if user == None: user = request.user
    users = User.objects.all()
    if user == "admin": user = "admin@gmail.com"
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