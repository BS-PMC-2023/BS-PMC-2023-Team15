from django.shortcuts import render

from database.models import Student


# Create your views here.

# return basic html header
def home(request):
    return render(request, 'home.html', {"users" : Student.objects.all()})