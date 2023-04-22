from database.models import Category, Equipment, IssueReport
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.shortcuts import get_object_or_404
from database.models import Reservation, Student
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date

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
def malfunction_view(request):
    return render(request, 'malfunction.html', {})

@login_required
def category_view(request, category):
    # category = Category.objects.get(name=category)
    items = Equipment.objects.filter(category=category)
    return render(request, 'catalog.html', {"items": items})

@login_required
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
        except ValueError:
            return HttpResponse("Invalid date format")

        if date_from > date_to :
            return HttpResponse("Invalid date range")

        # Process the form data as required
        student = Student.objects.get(id=student_id)
        item = Equipment.objects.get(serial_number=item_serial_number)
        reservation = Reservation(student=student, item=item, date_from=date_from, date_to=date_to)
        reservation.save()


    result = Equipment.objects.get(serial_number=item)
    issues = IssueReport.objects.filter(item=result)
    date_min = datetime.now().date().isoformat()


    return render(request, 'details.html', {"form": form, "item": result, "issues": issues, "date_min": date_min})


def overdue(request):
    today = date.today()
    reservations = Reservation.objects.filter(returned=False, date_to__lt=today)
    context = {'reservations': reservations}
    return render(request, 'overdue.html', context)