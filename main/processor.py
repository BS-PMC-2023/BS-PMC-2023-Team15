from datetime import date

from database.models import Reservation


def index(request):
# get all reservations that passed the current date and not returned
    res = Reservation.objects.filter(date_to__lt=date.today(), returned=False)
    return {'overdue': res.count()}
