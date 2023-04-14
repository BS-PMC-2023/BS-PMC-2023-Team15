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


from django.shortcuts import render, redirect
from database.models import Reservation
from datetime import date


def reserve_item(request):
    if request.method == 'POST':
        # Get the relevant data from the request
        student_email = request.POST['student_email']
        student_id = request.POST['student_id']
        item_serial_number = request.POST['item_serial_number']
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']

        # Create a new Reservation object
        reservation = Reservation(student_email=student_email,
                                  student_id=student_id,
                                  item_serial_number=item_serial_number,
                                  date_from=date_from,
                                  date_to=date_to)

        # Save the Reservation object to the database
        reservation.save()

        # Redirect to a success page or return a success message
        return redirect('/products')  # Replace 'success_page' with the appropriate URL or view name

    # Render the reservation page
    return render(request, 'reserve.html')


