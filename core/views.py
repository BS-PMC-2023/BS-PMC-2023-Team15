from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Reservation


# Create your views here.

@login_required
def core_view(request):

    return render(request, 'base.html', {})
