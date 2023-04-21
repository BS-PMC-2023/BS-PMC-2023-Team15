from database.models import Category, Equipment, IssueReport
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.shortcuts import get_object_or_404
from database.models import Reservation, Student
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect


def main_view(request):
    return render(request, 'categories.html', {} )


def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'products.html', {'categories': categories})


def studio_view(request):
    return render(request, 'studio.html', {})


def podcast_view(request):
    return render(request, 'podcast.html', {})

def malfunction_view(request):
    return render(request, 'malfunction.html', {})


def category_view(request, category):
    # category = Category.objects.get(name=category)
    items = Equipment.objects.filter(category=category)
    return render(request, 'catalog.html', {"items": items})


def item_detail_view(request, item):
    # Get the category object based on the category name
    # item = get_object_or_404(Category, serial_number=item)
    form=ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            item_serial_number = form.cleaned_data['item_serial_number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            # Process the form data as required
            student = Student.objects.get(student_id=student_id)
            item = Equipment.objects.get(serial_number=item_serial_number)
            reservation = Reservation(student=student, item=item, date_from=date_from, date_to=date_to)
            reservation.save()

            # Redirect to a new URL after successful form submission
            return redirect('products')


    result = Equipment.objects.get(serial_number=item)
    issues = IssueReport.objects.filter(item=result)
    date_min = datetime.now().date().isoformat()

    return render(request, 'details.html', {"form": form, "item": result, "issues": issues, "date_min": date_min})


def reserve_item(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            item_serial_number = form.cleaned_data['item_serial_number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            # Process the form data as required
            student = Student.objects.get(student_id=student_id)
            item = Equipment.objects.get(serial_number=item_serial_number)
            reservation = Reservation(student=student, item=item, date_from=date_from, date_to=date_to)
            reservation.save()

            # Redirect to a new URL after successful form submission
            return redirect('products')
    else:
        form = ReservationForm()

    return render(request, 'catalog.html')
