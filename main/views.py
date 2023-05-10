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
from django.views.decorators.http import require_http_methods

@login_required
def main_view(request):
    return render(request, 'categories.html', {} )

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
        # if form.is_valid():
        student_id = 123 #TODO: get student id from session cookie
        item_serial_number = item
        date_from = form.data['date_from']
        date_to = form.data['date_to']

        # catch ValidationError
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            if date_from > date_to: raise ArithmeticError
            # Process the form data as required
            student = Student.objects.get(id=student_id)
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


    return render(request, 'details.html', {"form": form, "item": result, "issues": issues, "date_min": date_min})


def overdue(request):
    today = date.today()
    reservations = Reservation.objects.filter(returned=False, date_to__lt=today)
    context = {'reservations': reservations}
    return render(request, 'overdue.html', context)


def profile_view(request):

    my_items = Reservation.objects.filter(student=123, returned=False)
    return render(request, 'profile.html', {"my_items": my_items})

def profile_return(request,item):
    if request.method != "POST":
        return redirect('main')
    reservation = Reservation.objects.get(id=item, student=123)
    reservation.returned = True
    reservation.save()
    return redirect('profile')