from django.shortcuts import render

from database.models import Category, Equipment
# Create your views here.
def core_view(request):
    return render(request, 'base.html', {})

