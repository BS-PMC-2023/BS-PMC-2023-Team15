from django.shortcuts import render
from database.models import Category, Equipment,Reservation
from django.shortcuts import render, redirect
from .forms import ReservationForm
# Create your views here.

def main_view(request):
    return render(request, 'categories.html', {} )


def product_view(request):
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
    return render(request, 'catalog.html', {"items":items})


def item_view(request):
    return render(request, 'details.html', {
    })


def reserve_item(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # student_email = form.cleaned_data['student_email']
            student_id = form.cleaned_data['student_id']
            item_serial_number = form.cleaned_data['item_serial_number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            reservation = Reservation( student_id=student_id, item_serial_number=item_serial_number, date_from=date_from, date_to=date_to)
            reservation.save()
            return redirect('reserve_item')
    else:
        form = ReservationForm()
    return render(request, 'reserve.html', {'form': form})




